# import pandas as pd
# import os
# from sklearn.preprocessing import MinMaxScaler
#
#
# folder_path = "D:\VietnameseMusicGenreClassification"
# new_folder_path = "D:\VietnameseMusicGenreClassification\data_normalization"
#
# # Cột loại bỏ
# exclude_columns = set(["index", "filename", "label", "h"])
#
# for filename in os.listdir(folder_path):
#     if filename.endswith(".csv"):
#         # Đọc file CSV
#         df_temp = pd.read_csv(os.path.join(folder_path, filename))
#
#         # Thực hiện normalization
#         for col in df_temp.columns:
#             if col not in exclude_columns:  # Check if column is not in excluded set
#                 scaler = MinMaxScaler()
#                 df_temp[col] = scaler.fit_transform(df_temp[[col]])
#
#         # Cập nhật dữ liệu (save to new file with "_normalized" suffix)
#         new_filename = os.path.splitext(filename)[0] + "_normalized.csv"
#         df_temp.to_csv(os.path.join(new_folder_path, new_filename), index=False)
#
# print("Normalization completed!")
#----------------------Normalization data-----------------
import pandas as pd
import os


folder_path = "D:\VietnameseMusicGenreClassification\data_normalization"

#tạo mảng lưu trữ toàn bộ data
all_data = []

#duyệt qua toàn bộ file .csv trong folder_path
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):

        #đọc file .csv
        data = pd.read_csv(os.path.join(folder_path, filename))

        #xóa bỏ cột filename
        data = data.drop(columns="filename")

        #thêm data vào all_data
        all_data.append(data)

#tổng hợp data
data = pd.concat(all_data, ignore_index=True)

#------gán nhãn genre thành số------
label_genre = {'ballad': 0, 'bolero': 1, 'hiphop': 2, 'kid': 3, 'rb': 4, 'red': 5, 'rock': 6}

data['label'] = data['label'].map(label_genre)

# data.to_csv('data_processed.csv', index=False)

print(data)

#----chia data thành tập train và tập test-----

from sklearn.model_selection import train_test_split

X = data.drop('label', axis=1)
Y = data['label']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Done data set")


#---------KNN------------
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, Y_train)



y_pred = knn.predict(X_test)


from sklearn.metrics import f1_score

micro_f1 = f1_score(Y_test, y_pred, average='micro')

print('Micro F1 (KNN): ', micro_f1)



#----------------SVC-----------
from sklearn.svm import SVC

# Tạo và huấn luyện mô hình SVM
svc = SVC()
svc.fit(X_train, Y_train)

# Dự đoán trên tập test và tính toán Micro F1
y_pred = svc.predict(X_test)
micro_f1 = f1_score(Y_test, y_pred, average='micro')
print('Micro F1 (SVM):', micro_f1)





#-------------Random forest-----------
from sklearn.ensemble import RandomForestClassifier

# Tạo và huấn luyện mô hình Random Forest với n_estimators=100
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, Y_train)

# Dự đoán trên tập test và tính toán Micro F1
y_pred = rf.predict(X_test)
micro_f1 = f1_score(Y_test, y_pred, average='micro')
print('Micro F1 (Random Forest):', micro_f1)



#-----------Gradient Boosting-------
from sklearn.ensemble import GradientBoostingClassifier

# Tạo và huấn luyện mô hình Gradient Boosting với n_estimators=100
gbm = GradientBoostingClassifier(n_estimators=100)
gbm.fit(X_train, Y_train)

# Dự đoán trên tập test và tính toán Micro F1
y_pred = gbm.predict(X_test)
micro_f1 = f1_score(Y_test, y_pred, average='micro')
print('Micro F1 (Gradient Boosting):', micro_f1)






#
