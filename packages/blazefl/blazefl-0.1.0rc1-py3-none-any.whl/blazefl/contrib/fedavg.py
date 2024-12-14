import random
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from blazefl.core import (
    ModelSelector,
    ParallelClientTrainer,
    PartitionedDataset,
    SerialClientTrainer,
    ServerHandler,
)
from blazefl.utils import (
    RandomState,
    deserialize_model,
    seed_everything,
    serialize_model,
)


@dataclass
class FedAvgUplinkPackage:
    model_parameters: torch.Tensor
    data_size: int
    metadata: dict | None = None


@dataclass
class FedAvgDownlinkPackage:
    model_parameters: torch.Tensor


class FedAvgServerHandler(ServerHandler):
    def __init__(
        self,
        model_selector: ModelSelector,
        model_name: str,
        dataset: PartitionedDataset,
        global_round: int,
        num_clients: int,
        sample_ratio: float,
        device: str,
    ) -> None:
        self.model = model_selector.select_model(model_name)
        self.dataset = dataset
        self.global_round = global_round
        self.num_clients = num_clients
        self.sample_ratio = sample_ratio
        self.device = device

        self.client_buffer_cache: list[FedAvgUplinkPackage] = []
        self.num_clients_per_round = int(self.num_clients * self.sample_ratio)
        self.round = 0

    def sample_clients(self) -> list[int]:
        sampled_clients = random.sample(
            range(self.num_clients), self.num_clients_per_round
        )

        return sorted(sampled_clients)

    def if_stop(self) -> bool:
        return self.round >= self.global_round

    def load(self, payload: FedAvgUplinkPackage) -> bool:
        self.client_buffer_cache.append(payload)

        if len(self.client_buffer_cache) == self.num_clients_per_round:
            self.global_update(self.client_buffer_cache)
            self.round += 1
            self.client_buffer_cache = []
            return True
        else:
            return False

    def global_update(self, buffer: list[FedAvgUplinkPackage]) -> None:
        parameters_list = [ele.model_parameters for ele in buffer]
        weights_list = [ele.data_size for ele in buffer]
        serialized_parameters = self.aggregate(parameters_list, weights_list)
        deserialize_model(self.model, serialized_parameters)

    @staticmethod
    def aggregate(
        parameters_list: list[torch.Tensor], weights_list: list[int]
    ) -> torch.Tensor:
        parameters = torch.stack(parameters_list, dim=-1)
        weights = torch.tensor(weights_list)
        weights = weights / torch.sum(weights)

        serialized_parameters = torch.sum(parameters * weights, dim=-1)

        return serialized_parameters

    def downlink_package(self) -> FedAvgDownlinkPackage:
        model_parameters = serialize_model(self.model)
        return FedAvgDownlinkPackage(model_parameters)


class FedAvgSerialClientTrainer(
    SerialClientTrainer[FedAvgUplinkPackage, FedAvgDownlinkPackage]
):
    def __init__(
        self,
        model_selector: ModelSelector,
        model_name: str,
        dataset: PartitionedDataset,
        device: str,
        num_clients: int,
        epochs: int,
        batch_size: int,
        lr: float,
    ) -> None:
        self.model = model_selector.select_model(model_name)
        self.dataset = dataset
        self.device = device
        self.num_clients = num_clients
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr

        self.model.to(self.device)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)
        self.criterion = torch.nn.CrossEntropyLoss()
        self.cache: list[FedAvgUplinkPackage] = []

    def local_process(
        self, payload: FedAvgDownlinkPackage, cid_list: list[int]
    ) -> None:
        model_parameters = payload.model_parameters
        for cid in tqdm(cid_list, desc="Client", leave=False):
            data_loader = self.dataset.get_dataloader(
                type_="train", cid=cid, batch_size=self.batch_size
            )
            pack = self.train(model_parameters, data_loader)
            val_loader = self.dataset.get_dataloader(
                type_="val", cid=cid, batch_size=self.batch_size
            )
            loss, acc = self.evaluate(val_loader)
            pack.metadata = {"loss": loss, "acc": acc}
            self.cache.append(pack)

    def train(
        self, model_parameters: torch.Tensor, train_loader: DataLoader
    ) -> FedAvgUplinkPackage:
        deserialize_model(self.model, model_parameters)
        self.model.train()

        data_size = 0
        for _ in range(self.epochs):
            for data, target in train_loader:
                data = data.to(self.device)
                target = target.to(self.device)

                output = self.model(data)
                loss = self.criterion(output, target)

                data_size += len(target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        model_parameters = serialize_model(self.model)

        return FedAvgUplinkPackage(model_parameters, data_size)

    def evaluate(self, test_loader: DataLoader) -> tuple[float, float]:
        self.model.eval()

        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)

                _, predicted = torch.max(outputs, 1)
                correct = torch.sum(predicted.eq(labels)).item()

                batch_size = labels.size(0)
                total_loss += loss.item() * batch_size
                total_correct += int(correct)
                total_samples += batch_size

        avg_loss = total_loss / total_samples
        avg_acc = total_correct / total_samples

        return avg_loss, avg_acc

    def uplink_package(self) -> list[FedAvgUplinkPackage]:
        package = deepcopy(self.cache)
        self.cache = []
        return package


@dataclass
class FedAvgDiskSharedData:
    model_selector: ModelSelector
    model_name: str
    dataset: PartitionedDataset
    epochs: int
    batch_size: int
    lr: float
    device: str
    cid: int
    seed: int
    payload: FedAvgDownlinkPackage
    state_path: Path


class FedAvgParalleClientTrainer(
    ParallelClientTrainer[
        FedAvgUplinkPackage, FedAvgDownlinkPackage, FedAvgDiskSharedData
    ]
):
    def __init__(
        self,
        model_selector: ModelSelector,
        model_name: str,
        share_dir: Path,
        state_dir: Path,
        dataset: PartitionedDataset,
        device: str,
        num_clients: int,
        epochs: int,
        batch_size: int,
        lr: float,
        seed: int,
        num_parallels: int,
    ) -> None:
        super().__init__(num_parallels, share_dir)
        self.model_selector = model_selector
        self.model_name = model_name
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.dataset = dataset
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.device = device
        self.num_clients = num_clients
        self.seed = seed

        if self.device == "cuda":
            self.device_count = torch.cuda.device_count()

    @staticmethod
    def process_client(path: Path) -> Path:
        data = torch.load(path, weights_only=False)
        assert isinstance(data, FedAvgDiskSharedData)

        if data.state_path.exists():
            state = torch.load(data.state_path, weights_only=False)
            assert isinstance(state, RandomState)
            RandomState.set_random_state(state)
        else:
            seed_everything(data.seed, device=data.device)

        model = data.model_selector.select_model(data.model_name)
        train_loader = data.dataset.get_dataloader(
            type_="train",
            cid=data.cid,
            batch_size=data.batch_size,
        )
        package = FedAvgParalleClientTrainer.train(
            model=model,
            model_parameters=data.payload.model_parameters,
            train_loader=train_loader,
            device=data.device,
            epochs=data.epochs,
            lr=data.lr,
        )
        val_loader = data.dataset.get_dataloader(
            type_="val",
            cid=data.cid,
            batch_size=data.batch_size,
        )
        loss, acc = FedAvgParalleClientTrainer.evaulate(
            model=model,
            test_loader=val_loader,
            device=data.device,
        )
        package.metadata = {"loss": loss, "acc": acc}
        torch.save(package, path)
        torch.save(RandomState.get_random_state(device=data.device), data.state_path)
        return path

    @staticmethod
    def train(
        model: torch.nn.Module,
        model_parameters: torch.Tensor,
        train_loader: DataLoader,
        device: str,
        epochs: int,
        lr: float,
    ) -> FedAvgUplinkPackage:
        model.to(device)
        deserialize_model(model, model_parameters)
        model.train()
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)
        criterion = torch.nn.CrossEntropyLoss()

        data_size = 0
        for _ in range(epochs):
            for data, target in train_loader:
                data = data.to(device)
                target = target.to(device)

                output = model(data)
                loss = criterion(output, target)

                data_size += len(target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        model_parameters = serialize_model(model)

        return FedAvgUplinkPackage(model_parameters, data_size)

    @staticmethod
    def evaulate(
        model: torch.nn.Module, test_loader: DataLoader, device: str
    ) -> tuple[float, float]:
        model.to(device)
        model.eval()
        criterion = torch.nn.CrossEntropyLoss()

        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                outputs = model(inputs)
                loss = criterion(outputs, labels)

                _, predicted = torch.max(outputs, 1)
                correct = torch.sum(predicted.eq(labels)).item()

                batch_size = labels.size(0)
                total_loss += loss.item() * batch_size
                total_correct += int(correct)
                total_samples += batch_size

        avg_loss = total_loss / total_samples
        avg_acc = total_correct / total_samples

        return avg_loss, avg_acc

    def get_shared_data(
        self, cid: int, payload: FedAvgDownlinkPackage
    ) -> FedAvgDiskSharedData:
        if self.device == "cuda":
            device = f"cuda:{cid % self.device_count}"
        else:
            device = self.device
        data = FedAvgDiskSharedData(
            model_selector=self.model_selector,
            model_name=self.model_name,
            dataset=self.dataset,
            epochs=self.epochs,
            batch_size=self.batch_size,
            lr=self.lr,
            device=device,
            cid=cid,
            seed=self.seed,
            payload=payload,
            state_path=self.state_dir.joinpath(f"{cid}.pt"),
        )
        return data

    def uplink_package(self) -> list[FedAvgUplinkPackage]:
        package = deepcopy(self.cache)
        self.cache = []
        return package
