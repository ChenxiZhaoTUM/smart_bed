def __getitem__(self, idx):
    datai = self.read_datai(idx)
    return datai[0:3], datai[3:], self.datafiles[idx]