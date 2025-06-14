import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os
from glob import glob

# 컬러맵 설정
cmap = cm._colormaps['RdYlGn_r']  # 초록 → 노랑 → 빨강

# 측정 컬럼 목록
measure_cols = ['Voltage_measured', 'Current_measured', 'Temperature_measured', 'Current_load', 'Voltage_load']

# 모든 배터리 CSV 파일 경로
csv_files = glob("./merged/B*.csv")

for file_path in csv_files:
    battery_id = os.path.splitext(os.path.basename(file_path))[0]
    print(f"📊 처리 중: {battery_id}")

    # 데이터 불러오기
    df = pd.read_csv(file_path)

    # 저장 폴더 생성
    output_dir = f"./images/{battery_id}"
    os.makedirs(output_dir, exist_ok=True)

    # 컬러 정규화
    norm = mcolors.Normalize(vmin=df['cycle_idx'].min(), vmax=df['cycle_idx'].max())

    # 그래프 생성 및 저장
    for col in measure_cols:
        fig, ax = plt.subplots(figsize=(12, 5))
        for cycle_idx, group in df.groupby("cycle_idx"):
            color = cmap(norm(cycle_idx))
            ax.plot(group["Time"], group[col], color=color, alpha=0.5)

        ax.set_title(f"battery:{battery_id} {col} vs Time (Colored by Cycle)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(col)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Cycle Index')

        ax.grid(True)
        plt.tight_layout()

        # 저장
        save_path = os.path.join(output_dir, f"{battery_id}_{col}.png")
        plt.savefig(save_path, dpi=300)
        plt.close()

print("✅ 모든 배터리 그래프 저장 완료!")
