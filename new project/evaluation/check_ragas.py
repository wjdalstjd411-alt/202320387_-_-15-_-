import ragas
print("Ragas Version:", ragas.__version__)

from ragas import metrics

print("\nAvailable Metrics:")
for name in dir(metrics):
    if not name.startswith("_"):
        print(name)