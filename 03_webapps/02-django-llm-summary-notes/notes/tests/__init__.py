"""
PyCharmCEで「Python tests（unittest）」構成で実行する場合、
manage.py が通らないため Django 初期化と「テストDBの準備」を
ここで肩代わりする処理
"""
import os
import atexit
import django
from django.apps import apps
from django.test.utils import (
    setup_test_environment, teardown_test_environment,
    setup_databases, teardown_databases,
)

# 1) 設定モジュールを指定（manage.py を通らないため自前でセット）
#    プロジェクトに合わせてモジュールパスを変更してください
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# 2) Django 起動
#    manage.py 経由で走った場合など「既に起動済み」の可能性があるため
#    apps.ready を見て二重初期化を防止（re-entrant エラー回避）
if not apps.ready:
    django.setup()

# 3) テスト環境のセットアップ
setup_test_environment()

# 4) テストDBを作成
#    DJANGO_KEEPDB=1 を環境変数に入れると DB を使い回して高速化（--keepdb 相当）
_KEEPDB = os.environ.get("DJANGO_KEEPDB", "").lower() in ("1", "true", "yes")
_OLD_CONFIG = setup_databases(verbosity=1, interactive=False, keepdb=_KEEPDB)

# 5) 終了時にクリーンアップ
#    - 普段は drop してクリーンに戻す
#    - 高速化したいときは DJANGO_KEEPDB=1 を付けて drop しない
def _teardown():
    if not _KEEPDB:
        teardown_databases(_OLD_CONFIG, verbosity=1)
    teardown_test_environment()

# プロセス終了時に必ず実行
atexit.register(_teardown)
