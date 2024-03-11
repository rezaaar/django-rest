from sklearn.linear_model import LogisticRegression

# Sample data (replace with your actual data)
X = [[25, 80000], [32, 60000], [40, 90000], [28, 50000], [35, 70000]]
y = [0, 1, 1, 0, 1]

model = LogisticRegression()
model.fit(X, y)

def predict(data):
    data = [data]
    prediction = model.predict(data)[0]
    return prediction
