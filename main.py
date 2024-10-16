from supabase import create_client, Client
import requests

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

# Supabaseのnew_productsテーブルからデータを取得
def get_new_products_from_supabase():
    try:
        # new_productsテーブルから全てのデータを取得
        response = supabase.table("new_products").select("*").execute()
        data = response.data
        return data
    except Exception as e:
        print(f"Error fetching data from Supabase: {e}")
        return []

# メイン処理
def main():
    # Supabaseから新商品のデータを取得
    new_products = get_new_products_from_supabase()

    # 新商品が存在するか確認
    if new_products:
        # 各新商品を整形してLINEでブロードキャスト送信
        for product in new_products:
            message = (
                f"商品名: {product['product_name']}\n"
                f"発売開始日: {product['release_date']}\n"
                f"作り方画像: {product['recipe_image_url']}"
            )
            send_broadcast_message(message)
    else:
        print("No new products to broadcast.")

# スクリプトを実行
if __name__ == "__main__":
    main()