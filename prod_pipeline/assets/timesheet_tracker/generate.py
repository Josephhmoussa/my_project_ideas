# import pandas as pd
# from datetime import date, timedelta
# import random

# random.seed(42)

# # 52 Mondays for 2026
# start = date(2026, 1, 5)
# weeks = [start + timedelta(weeks=i) for i in range(52)]
# week_labels = [d.strftime("%-d-%b") for d in weeks]

# org = "Infrastructure & Technology: 10100_DEMO ORG"

# employees_data = [
#     # --- Sarah Mitchell's team (5 people) ---
#     ("Sarah Mitchell", 10101, "James Thornton", [
#         ("PROJ-A1", "A1.10"), ("PROJ-A1", "A1.20"), ("PROJ-B2", "B2.01"), ("ADMIN", "1C"),
#     ]),
#     ("Sarah Mitchell", 10102, "Clara Nguyen", [
#         ("PROJ-A1", "A1.10"), ("PROJ-B2", "B2.01"), ("PROJ-B2", "B2.05"), ("ADMIN", "1C"),
#     ]),
#     ("Sarah Mitchell", 10103, "Daniel Park", [
#         ("PROJ-A1", "A1.20"), ("PROJ-C3", "C3.01"), ("ADMIN", "1C"),
#     ]),
#     ("Sarah Mitchell", 10104, "Nina Castillo", [
#         ("PROJ-C3", "C3.01"), ("PROJ-C3", "C3.02"), ("ADMIN", "1C"), ("ADMIN", "1D"),
#     ]),
#     ("Sarah Mitchell", 10105, "Ethan Brooks", [
#         ("PROJ-B2", "B2.05"), ("PROJ-C3", "C3.02"), ("ADMIN", "1C"),
#     ]),

#     # --- David Okafor's team (7 people) ---
#     ("David Okafor", 10106, "Marcus Reid", [
#         ("PROJ-D4", "D4.00.10"), ("PROJ-D4", "D4.21.10"), ("ADMIN", "1C"), ("ADMIN", "1D"),
#     ]),
#     ("David Okafor", 10107, "Priya Sharma", [
#         ("PROJ-D4", "D4.00.10"), ("PROJ-D4", "D4.21.10"), ("ADMIN", "1C"),
#     ]),
#     ("David Okafor", 10108, "Lucas Ferreira", [
#         ("PROJ-D4", "D4.00.10"), ("PROJ-E5", "E5.00.10"), ("ADMIN", "1C"),
#     ]),
#     ("David Okafor", 10109, "Hana Kovac", [
#         ("PROJ-E5", "E5.00.10"), ("PROJ-E5", "E5.11.10"), ("ADMIN", "1C"),
#     ]),
#     ("David Okafor", 10110, "Omar Bensaid", [
#         ("PROJ-E5", "E5.11.10"), ("PROJ-D4", "D4.21.10"), ("ADMIN", "1C"),
#     ]),
#     ("David Okafor", 10111, "Sofia Andersen", [
#         ("PROJ-E5", "E5.00.10"), ("PROJ-E5", "E5.11.10"), ("ADMIN", "1C"),
#     ]),
#     ("David Okafor", 10112, "Raj Patel", [
#         ("PROJ-D4", "D4.00.10"), ("PROJ-D4", "D4.21.10"), ("ADMIN", "1C"),
#     ]),

#     # --- Rachel Burns' team (8 people) ---
#     ("Rachel Burns", 10113, "Yuki Tanaka", [
#         ("PROJ-F6", "F6.10.00"), ("PROJ-F6", "F6.10.01"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10114, "Leo Dupont", [
#         ("PROJ-F6", "F6.10.00"), ("PROJ-G7", "G7.00.10"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10115, "Amira Hassan", [
#         ("PROJ-G7", "G7.00.10"), ("PROJ-G7", "G7.21.10"), ("ADMIN", "1C"), ("ADMIN", "1D"),
#     ]),
#     ("Rachel Burns", 10116, "Tom Eriksson", [
#         ("PROJ-G7", "G7.00.10"), ("PROJ-G7", "G7.21.10"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10117, "Mei Lin", [
#         ("PROJ-F6", "F6.10.01"), ("PROJ-G7", "G7.21.10"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10118, "Carlos Vega", [
#         ("PROJ-H8", "H8.00.10"), ("PROJ-H8", "H8.10.01"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10119, "Fatima Diallo", [
#         ("PROJ-H8", "H8.00.10"), ("PROJ-H8", "H8.10.01"), ("ADMIN", "1C"),
#     ]),
#     ("Rachel Burns", 10120, "Ivan Petrov", [
#         ("PROJ-H8", "H8.10.01"), ("PROJ-F6", "F6.10.00"), ("ADMIN", "1C"),
#     ]),
# ]

# def distribute_hours(n_work_tasks, total=40):
#     admin = random.choice([0, 8, 8, 8])
#     remaining = total - admin
#     if n_work_tasks == 1:
#         work = [remaining]
#     else:
#         cuts = sorted(random.sample(range(4, remaining - 4 * (n_work_tasks - 1)), n_work_tasks - 1))
#         cuts = [0] + cuts + [remaining]
#         work = [cuts[i+1] - cuts[i] for i in range(n_work_tasks)]
#     return work + [admin]

# def assign_week_statuses():
#     """Per week: ~75% submitted, ~15% not created, ~10% saved but not submitted."""
#     statuses = []
#     for _ in range(52):
#         r = random.random()
#         if r < 0.75:
#             statuses.append("submitted")
#         elif r < 0.90:
#             statuses.append("not_created")
#         else:
#             statuses.append("saved_not_submitted")
#     return statuses

# base_cols = ["Org Level 4 Name", "Organization", "Manager", "Employee ID", "Employee Name"]

# submitted_rows = []
# not_created_rows = []
# saved_not_sub_rows = []

# for manager, emp_id, emp_name, tasks in employees_data:
#     n_work = len(tasks) - 1
#     weekly_hours = [distribute_hours(n_work) for _ in range(52)]
#     week_statuses = assign_week_statuses()

#     week_totals = [sum(weekly_hours[w]) for w in range(52)]  # total hours per week across all tasks

#     base = {
#         "Org Level 4 Name": org,
#         "Organization": org,
#         "Manager": manager,
#         "Employee ID": emp_id,
#         "Employee Name": emp_name,
#     }

#     # --- CSV 1: per-task rows, submitted weeks only ---
#     for t_idx, (proj, task) in enumerate(tasks):
#         row = {**base, "Project Number": proj, "Task Number": task}
#         for w_idx, label in enumerate(week_labels):
#             if week_statuses[w_idx] == "submitted":
#                 h = weekly_hours[w_idx][t_idx]
#                 row[label] = h if h > 0 else None
#             else:
#                 row[label] = None
#         row["Grand Total"] = sum(
#             weekly_hours[w][t_idx]
#             for w in range(52)
#             if week_statuses[w] == "submitted" and weekly_hours[w][t_idx]
#         )
#         submitted_rows.append(row)

#     # Subtotal row for CSV 1
#     subtotal = {**base, "Project Number": "", "Task Number": ""}
#     for w_idx, label in enumerate(week_labels):
#         subtotal[label] = 40 if week_statuses[w_idx] == "submitted" else None
#     subtotal["Grand Total"] = sum(1 for s in week_statuses if s == "submitted") * 40
#     submitted_rows.append(subtotal)

#     # --- CSV 2: one row per employee, hours only in not-created weeks ---
#     nc_row = {**base}
#     for w_idx, label in enumerate(week_labels):
#         nc_row[label] = week_totals[w_idx] if week_statuses[w_idx] == "not_created" else None
#     nc_row["Grand Total"] = sum(
#         week_totals[w] for w in range(52) if week_statuses[w] == "not_created"
#     ) or None
#     # Only include employees who have at least one not-created week
#     if any(week_statuses[w] == "not_created" for w in range(52)):
#         not_created_rows.append(nc_row)

#     # --- CSV 3: one row per employee, hours only in saved-not-submitted weeks ---
#     sns_row = {**base}
#     for w_idx, label in enumerate(week_labels):
#         sns_row[label] = week_totals[w_idx] if week_statuses[w_idx] == "saved_not_submitted" else None
#     sns_row["Grand Total"] = sum(
#         week_totals[w] for w in range(52) if week_statuses[w] == "saved_not_submitted"
#     ) or None
#     # Only include employees who have at least one saved-not-submitted week
#     if any(week_statuses[w] == "saved_not_submitted" for w in range(52)):
#         saved_not_sub_rows.append(sns_row)

# # Grand Total summary rows for CSVs 2 & 3
# def grand_total_row(rows_list):
#     gt = {col: "" for col in base_cols}
#     gt["Org Level 4 Name"] = "Grand Total"
#     for label in week_labels:
#         vals = [r[label] for r in rows_list if r.get(label)]
#         gt[label] = sum(vals) if vals else None
#     gt["Grand Total"] = sum(r["Grand Total"] for r in rows_list if r.get("Grand Total"))
#     return gt

# not_created_rows.append(grand_total_row(not_created_rows))
# saved_not_sub_rows.append(grand_total_row(saved_not_sub_rows))

# # --- Output ---
# cols_main   = base_cols + ["Project Number", "Task Number"] + week_labels + ["Grand Total"]
# cols_report = base_cols + week_labels + ["Grand Total"]

# pd.DataFrame(submitted_rows, columns=cols_main).to_csv("timesheet_full_year_2026.csv", index=False)
# print(f"Created timesheet_full_year_2026.csv")

# pd.DataFrame(not_created_rows, columns=cols_report).to_csv("timesheet_missing_timecards_2026.csv", index=False)
# print(f"Created timesheet_missing_timecards_2026.csv")

# pd.DataFrame(saved_not_sub_rows, columns=cols_report).to_csv("timesheet_saved_not_submitted_2026.csv", index=False)
# print(f"Created timesheet_saved_not_submitted_2026.csv")

# import polars as pl

# output_csv = "/Users/josephmoussa/Desktop/my_project_ideas/prod_pipeline/assets/timesheet_tracker/lookup_files/task_codes.csv"
# output_csv2 = "/Users/josephmoussa/Desktop/my_project_ideas/prod_pipeline/assets/timesheet_tracker/lookup_files/project_codes_names.csv"

# df = pl.DataFrame(
#     {

#         "task_code": [
#             "A1.10",
#             "A1.20",
#             "B2.05",
#             "B2.01",
#             "C3.01",
#             "C3.02",
#             "D4.00.10",
#             "D4.21.10",
#             "E5.11.10",
#             "E5.00.10",
#             "F6.10.01",
#             "F6.10.00",
#             "G7.00.10",
#             "G7.21.10",
#             "H8.10.01",
#             "H8.00.10",
#             "1D - Leave & Absences",
#             "1C - Admin & Mgt"
#         ],

#         "cpx_opx": [
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Capex",
#             "Opex",
#             "Opex"
#         ]
#     }
# )

# df2 = pl.DataFrame(
#     {
#         "project_code": [
#             "A1",
#             "B2",
#             "C3",
#             "D4",
#             "E5",
#             "F6",
#             "G7",
#             "H8",
#             "ADMIN"
#         ],

#         "project_name": [
#             "Cloud Infrastructure Modernization",
#             "Platform Modernisation",
#             "Client Engagement",
#             "Data Analytics",
#             "Customer Data Platform",
#             "Cybersecurity Framework Uplift",
#             "Enterprise Resource Planning Migration",
#             "API Integration Hub",
#             "Global Admin"
#         ]
#     }
# )

# df.write_csv(output_csv)
# df2.write_csv(output_csv2)