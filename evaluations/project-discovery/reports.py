"""CSV reporting for the offline fixture."""

import csv
import io


def export_orders(orders, tenant, status=None):
    selected = [row for row in orders if status is None or row["status"] == status]
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["id", "status"])
    for row in selected:
        writer.writerow([row["id"], row["status"]])
    return output.getvalue()
