import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ฟังก์ชันสำหรับเลือกไฟล์ .csv
def select_csv_file():
    Tk().withdraw()  # ซ่อนหน้าต่าง Tkinter
    filename = askopenfilename(filetypes=[("CSV files", "*.csv")])
    return filename

# ฟังก์ชันสำหรับทำ Data Cleaning
def clean_data(df):
    print("เลือกวิธีการทำความสะอาดข้อมูล:")
    print("1. ลบแถวที่มีค่า NaN")
    print("2. เติมค่า NaN ด้วยค่าเฉลี่ย (Mean)")
    print("3. เติมค่า NaN ด้วยมัธยฐาน (Median)")

    choice = input("กรุณาเลือกตัวเลือก (1/2/3): ")

    if choice == '1':
        df_cleaned = df.dropna()
        print("ลบแถวที่มีค่า NaN เรียบร้อยแล้ว")
    elif choice == '2':
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df_cleaned = df.copy()
        df_cleaned[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        print("เติมค่า NaN ด้วยค่าเฉลี่ยเรียบร้อยแล้ว")
    elif choice == '3':
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df_cleaned = df.copy()
        df_cleaned[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        print("เติมค่า NaN ด้วยมัธยฐานเรียบร้อยแล้ว")
    else:
        print("ตัวเลือกไม่ถูกต้อง ใช้การลบแถวที่มีค่า NaN เป็นค่าเริ่มต้น")
        df_cleaned = df.dropna()

    return df_cleaned


# ฟังก์ชันสำหรับสร้างกราฟ
def create_graph(df):
    # สร้างกราฟ histogram ของแต่ละคอลัมน์ใน dataframe
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns  # เลือกเฉพาะคอลัมน์ที่เป็นตัวเลข
    df[num_columns].hist(figsize=(12, 10), color='skyblue', edgecolor='black', bins=15)

    # เพิ่ม Title, ชื่อแกน และรูปแบบกราฟให้ดูเป็นทางการ
    plt.suptitle('Data Distribution by Column', fontsize=16, fontweight='bold')

    for ax in plt.gcf().axes:  # สำหรับทุกแกนในกราฟ
        ax.set_xlabel(ax.get_xlabel(), fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(ax.get_title(), fontsize=14, fontweight='bold')
        ax.grid(False)  # ปิดเส้นตาราง

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # เว้นพื้นที่ให้ title ด้านบน
    plt.show()

# หลักการทำงาน
if __name__ == "__main__":
    csv_file = select_csv_file()
    if csv_file:
        data = pd.read_csv(csv_file)
        print("ข้อมูลก่อนการทำความสะอาด:")
        print(data.head())

        cleaned_data = clean_data(data)
        print("ข้อมูลหลังการทำความสะอาด:")
        print(cleaned_data.head())

        create_graph(cleaned_data)
