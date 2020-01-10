from UserItemData import UserItemData


class ViewsPredictor:
    def __init__(self):
        return

    def fit(self, x: UserItemData):
        self.data = x.data

    def predict(self, user_id: int):
        return self.data['movieID'].value_counts().to_dict()
