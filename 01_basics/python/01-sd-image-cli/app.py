import argparse
from pathlib import Path
from diffusers import DiffusionPipeline
from googletrans import Translator

"""
Stable Diffusion（diffusers）で画像を生成する最小スクリプト
- 日本語プロンプトは自動で英語に翻訳（--no_translate でスキップ可、実行時間短縮）
- height/width は 8 の倍数のみ許可
- 出力は png/jpg のみ（--img_format）
- 保存先ディレクトリは自動作成
※ 初回実行時はモデルのダウンロードが発生し、時間がかかる
"""


def build_options() -> argparse.Namespace:
    """コマンドライン引数の定義"""
    parser = argparse.ArgumentParser(description='Stable Diffusionで画像を生成します')
    parser.add_argument('--height', type=int, default=256,
                        help='生成画像の高さ（8で割り切れる必要があります）')
    parser.add_argument('--width', type=int, default=256,
                        help='生成画像の幅（8で割り切れる必要があります）')
    parser.add_argument('--filename', type=str, default='demo',
                        help='出力ファイル名')
    parser.add_argument('--img_format', type=str, default='png', choices=['png', 'jpg'],
                        help='出力フォーマット')
    parser.add_argument('--output_dir', type=str, default='outputs',
                        help='出力先ディレクトリ（存在しない場合は自動作成）')
    parser.add_argument('--no_translate', action='store_true',
                        help='翻訳を行わず、入力文字列をそのまま使用する')
    return parser.parse_args()


def validate_grid(height: int, width: int) -> None:
    """高さ・幅が8の倍数かを検証"""
    if height % 8 != 0 or width % 8 != 0:
        raise ValueError(
            f"height と width は8の倍数にしてください（現在: 高さ={height}, 幅={width}）。"
        )


def translate_to_en(text: str) -> str:
    """
    入力テキストを英語に翻訳する
    - src='auto'：日本語/英語など入力言語を自動判定
    - dest='en' ：最終的に英語へ（多くの拡散モデルは英語プロンプトで最適化）
    """
    translator = Translator()
    try:
        # 英語入力も安全に扱えるよう、自動判定→英語へ
        return translator.translate(text, src='auto', dest='en').text
    except Exception as err:
        print(f"[WARN] 翻訳に失敗しました。原文を使用します: {err}")
        return text


def render_and_save(
        prompt: str,
        height: int,
        width: int,
        filename: str,
        img_format: str,
        output_dir: str
) -> None:
    """
    画像を生成し、指定フォーマットで保存
      1) 出力フォーマットの正規化と検証
      2) 保存先ディレクトリの作成
      3) モデルの読み込み（初回はモデルダウンロードで時間がかかる）
      4) 画像生成
      5) 画像の保存
    """
    # 1) フォーマットの正規化・検証
    fmt = img_format.lower()
    if fmt not in ('png', 'jpg'):
        raise ValueError("img_format は 'png' または 'jpg' を指定してください。")
    image_format = "PNG" if fmt == "png" else "JPEG"

    # 2) 保存先の準備
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # filename から拡張子を取り除いて、--img_format に合わせた拡張子を付与
    target = out_dir / f"{Path(filename).stem}.{fmt}"

    # 3) モデル読込
    # from_pretrained は初回にモデル重みをダウンロードするため時間がかかる
    # ※ モデルを変更する場合は、下記の文字列を別のモデルIDに差し替えるだけでOK
    # 例）汎用（速さ重視）: "stabilityai/stable-diffusion-2-1"
    # 例）超速系(Turbo):  "stabilityai/sd-turbo"（steps=4, guidance=0.0 推奨）
    pipeline = DiffusionPipeline.from_pretrained("digiplay/AsianBrmBeautyrealmix_v2.0")

    # 4) 画像生成
    img = pipeline(prompt, height=height, width=width).images[0]

    # 5) 保存
    img.save(target.as_posix(), format=image_format)
    print(f"Saved {target} ({image_format})")


if __name__ == "__main__":
    # 引数の取得
    args = build_options()

    # 入力された高さ・幅の検証（8の倍数か）
    validate_grid(args.height, args.width)

    # プロンプト入力受取
    raw = input("どんな画像を生成しますか？: ").strip()

    # 翻訳の有無を切替
    final_prompt = raw if args.no_translate else translate_to_en(raw)

    # 生成と保存
    render_and_save(
        prompt=final_prompt,
        height=args.height,
        width=args.width,
        filename=args.filename,
        img_format=args.img_format,
        output_dir=args.output_dir,
    )
