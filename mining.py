"""Tái lập các con số bằng chứng cho canvas CP1 / spec §1 — VLearn Solo Arena.

Chạy:  python mining.py --csv <duong/dan/tutor_turns.csv>

Commit script và output vào repo nhóm. KHÔNG commit file CSV (quy định bảo mật data pack).
"""
import argparse

import pandas as pd

p = argparse.ArgumentParser()
p.add_argument('--csv', required=True, help='duong dan toi tutor_turns.csv')
a = p.parse_args()

df = pd.read_csv(a.csv)
k4 = df[df.cohort_hint == 'K4']
n, nk = len(df), len(k4)
print(f"Toan file: {n} luot | K4: {nk} luot, {k4.student.nunique()} hoc vien\n")

print("== 4 co che da thiet ke san nhung bo trong ==")
u = int(df.understanding_level.notna().sum())
print(f"understanding_level co du lieu : {u}/{n} ({u / n * 100:.2f}%)")
for m in ['suggest_next_topic', 'motivate', 'celebrate_progress']:
    c = int((df.move_used == m).sum())
    print(f"{m:22s}: {c}/{n} ({c / n * 100:.2f}%)")

print("\n== Tutor gan nhu chi lam mot viec: giang ==")
for m in ['review_concept', 'ask_probing_question', 'give_hint', 'validate_understanding']:
    c, ck = int((df.move_used == m).sum()), int((k4.move_used == m).sum())
    print(f"{m:22s}: toan file {c}/{n} ({c / n * 100:.1f}%) | K4 {ck}/{nk} ({ck / nk * 100:.2f}%)")

print("\n== Khong co hoat dong nao cho hoc vien LAM ==")
print(f"19 cot: {df.columns.tolist()}")

print("\n== Proxy roi bo ==")
v = k4.student.value_counts()
print(f"Hoc vien K4 chi hoi 1 lan: {int((v == 1).sum())}/{len(v)} ({(v == 1).mean() * 100:.1f}%)")

print("\n== Boi canh cho bang impact ==")
r = int(k4.rating.notna().sum())
hc = int((~k4.has_citation).sum())
ps = int(k4.is_preset.sum())
print(f"K4 co rating          : {r}/{nk} ({r / nk * 100:.2f}%)")
print(f"K4 khong trich dan    : {hc}/{nk} ({hc / nk * 100:.1f}%)")
print(f"K4 la cau mau (preset): {ps}/{nk} ({ps / nk * 100:.1f}%)")
