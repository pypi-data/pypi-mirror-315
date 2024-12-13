import torch as tr
from datetime import datetime


class Trainer:
    def __init__(
        self,
        model,
        lossf,
        opt,
        sch,
        epochn,
        device,
        train_dataloader,
        val_dataloader,
        test_dataloader,
    ):
        self.model = model
        self.lossf = lossf
        self.opt = opt
        self.sch = sch
        self.epochn = epochn
        self.device = device
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.test_dataloader = test_dataloader

        self.lossi = []
        self.val_lossi = []
        self.test_lossi = []

    def train(self):
        self.model.to(self.device)

        for epoch in range(self.epochn):
            self.model.train()

            print("-" * 80)
            print("| Epoch: %d |" % epoch)
            print(f"|*TRAIN*|")
            self.model.to(self.device)
            self.training_step()
            self.sch.step()

            self.model.eval()
            print(f"|*VALIDATION*|")
            self.validate()

        print("-" * 80)
        print("-" * 80)
        print("-" * 80)
        print(f"|*TEST*|")
        self.model.eval()
        self.test()

    def training_step(self):
        local_loss = []
        infon = 5000
        b_ts = datetime.now()
        for ix, (features, target) in enumerate(self.train_dataloader):
            self.opt.zero_grad()

            features = features.to(self.device)
            pred = self.model(features)
            target = target.to(self.device)

            loss = self.lossf(pred, target)
            loss.backward()
            self.opt.step()

            self.lossi.append(loss.item())
            local_loss.append(loss.item())

            if ix % infon == 0 and ix != 0:
                local_loss = tr.tensor(local_loss)
                e_ts = datetime.now()

                print(f"| train time of {infon} batches: {e_ts - b_ts} |")
                print(
                    f"| total train batch mean loss: {
                        tr.mean(local_loss)} |"
                )
                local_loss = []
                b_ts = e_ts

    def validate(self):
        local_loss = []
        b_ts = datetime.now()

        with tr.no_grad():
            for ix, (features, target) in enumerate(self.val_dataloader):
                features = features.to(self.device)
                pred = self.model(features)
                target = target.to(self.device)

                loss = self.lossf(pred, target)
                self.val_lossi.append(loss)
                local_loss.append(loss)
        local_loss = tr.tensor(local_loss)
        e_ts = datetime.now()
        print(f"| val time: {e_ts - b_ts}|")
        print(f"| val mean loss: {tr.mean(local_loss)} |")

    def test(self):
        b_ts = datetime.now()
        with tr.no_grad():
            for ix, (features, target) in enumerate(self.test_dataloader):
                features = features.to(self.device)
                pred = self.model(features)
                target = target.to(self.device)

                loss = self.lossf(pred, target)

                self.test_lossi.append(loss)

        local_loss = tr.tensor(self.test_lossi)
        e_ts = datetime.now()
        print(f"test time: {e_ts - b_ts}")
        print(f"| test mean loss: {tr.mean(local_loss)} |")

    def get_metadata(self):
        return self.lossi, self.val_lossi, self.test_lossi
