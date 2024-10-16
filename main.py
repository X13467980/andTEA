from supabase import create_client, Client
import requests
import os

# SupabaseのURLとAPIキーを設定
url: str = "https://wdtbvjtmuvqevoayjvwx.supabase.co"
api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkdGJ2anRtdXZxZXZvYXlqdnd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkwNzE2MzQsImV4cCI6MjA0NDY0NzYzNH0.b3Ysqzy2Ag9c72QoAk4DjCwhsF9yu6A--K1__yfJfVw"

# LINEのアクセストークンを設定
line_access_token = 'XUfxX0Ag6Rrvva289R1w/pNJ7wPPwzB8J+/LtYPZgiXBJNkXwfgrRW92PYT1aFz/DS469dnj8yj3usa76uAfNqHM/ISFeLKJTQXEAgU1LbH4o8Gk9TyT80t126Sq+iZkEms8U6Bctl5i1/0UlCn9TwdB04t89/1O/w1cDnyilFU='


# Supabaseクライアントを作成
supabase: Client = create_client(url, api_key)

# LINEブロードキャストメッセージを送信する関数
def send_broadcast_message(message: str):
    url = 'https://api.line.me/v2/bot/message/broadcast'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_access_token}'
    }

    payload = {
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Broadcast message sent successfully")
    else:
        print(f"Failed to send broadcast message: {response.status_code}, {response.text}")

# 前回送信した商品のIDをファイルから読み込む
def get_last_sent_id(file_path='last_sent_id.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    return None

# 新しく送信した商品のIDをファイルに保存する
def set_last_sent_id(last_id, file_path='last_sent_id.txt'):
    with open(file_path, 'w') as file:
        file.write(str(last_id))

# Supabaseのnew_productsテーブルから新しく追加された商品を取得
def get_new_products_from_supabase(last_sent_id):
    try:
        # 前回送信したIDより大きいIDを持つ新商品を取得
        if last_sent_id:
            response = supabase.table("new_products").select("*").gt('id', last_sent_id).execute()
        else:
            response = supabase.table("new_products").select("*").execute()
        data = response.data
        return data
    except Exception as e:
        print(f"Error fetching data from Supabase: {e}")
        return []

# メイン処理
def main():
    # 前回送信した最新の商品IDを取得
    last_sent_id = get_last_sent_id()

    # Supabaseから新商品のデータを取得（前回送信したID以降のもの）
    new_products = get_new_products_from_supabase(last_sent_id)

    # 新商品が存在するか確認
    if new_products:
        # 最後に送信した商品のIDを追跡するために、最新IDを記録
        latest_id = None

        # 各新商品を整形してLINEでブロードキャスト送信
        for product in new_products:
            message = (
                f"商品名: {product['product_name']}\n"
                f"発売開始日: {product['release_date']}\n"
                f"作り方画像: {product['recipe_image_url']}"
            )
            send_broadcast_message(message)
            # 最新のIDを更新
            latest_id = product['id']

        # 送信が完了したら、最後に送信した商品のIDをファイルに保存
        if latest_id:
            set_last_sent_id(latest_id)
    else:
        print("No new products to broadcast.")

# スクリプトを実行
if __name__ == "__main__":
    main()