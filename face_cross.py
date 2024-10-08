import os
import cv2

def draw_cross_on_faces(input_image_filename, output_image_filename):
    # 画像の読み込み
    image = cv2.imread(input_image_filename)
    if image is None:
        print(f"画像 '{input_image_filename}' を読み込めませんでした。")
        return

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Haar Cascadeの分類器を読み込む（相対パスを使用）
    cascade_relative_path = os.path.join(
        '.venv', 'Lib', 'site-packages', 'cv2', 'data', 'haarcascade_frontalface_default.xml'
    )
    face_cascade = cv2.CascadeClassifier(cascade_relative_path)

    if face_cascade.empty():
        print(f"分類器を読み込めませんでした。パスを確認してください: {cascade_relative_path}")
        return

    # 顔の検出
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # 顔にバツ印を描画
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # 左上から右下への線
            cv2.line(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # 右上から左下への線
            cv2.line(image, (x + w, y), (x, y + h), (0, 0, 255), 2)
        print(f"'{input_image_filename}' において {len(faces)} 個の顔にバツ印を描画しました。")
    else:
        print(f"'{input_image_filename}' で顔が検出されませんでした。")

    # 処理後の画像を保存
    cv2.imwrite(output_image_filename, image)
    print(f"処理後の画像を '{output_image_filename}' として保存しました。")

if __name__ == "__main__":
    # カレントディレクトリ内のファイルを取得
    files = os.listdir('.')
    for filename in files:
        # 'input' が付いているファイルを検索
        if filename.startswith('input'):
            # 拡張子をチェック（画像ファイルのみを対象）
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
                # 出力ファイル名を作成
                # 'input' を 'out' に置き換える
                output_filename = 'out' + filename[len('input'):]
                # 処理を実行
                draw_cross_on_faces(filename, output_filename)