"""
==============================================================================
Cloudflare R2 アップローダ
------------------------------------------------------------------------------
用途:
    Instagram 投稿用の画像を Cloudflare R2（S3 互換オブジェクトストレージ）に
    アップロードし、公開 URL を返す。Meta Graph API は外部 URL を要求するため
    画像ホスティングが必須。

前提:
    - R2 バケットを事前作成し、Public Bucket か R2.dev サブドメイン公開設定
    - API トークン（access key + secret）を取得
    - boto3 を S3 互換エンドポイントで利用

実行例:
    >>> from scripts.lib.r2_uploader import upload_image
    >>> url = upload_image(Path("/path/to/photo.jpg"))

関連 .env キー:
    R2_ACCOUNT_ID
    R2_ACCESS_KEY_ID
    R2_SECRET_ACCESS_KEY
    R2_BUCKET_NAME
    R2_PUBLIC_URL
==============================================================================
"""
from __future__ import annotations

import logging
import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

try:
    import boto3
    from botocore.config import Config as BotoConfig
except ImportError:  # pragma: no cover
    boto3 = None  # type: ignore[assignment]
    BotoConfig = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)


REQUIRED_ENVS = (
    "R2_ACCOUNT_ID",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_BUCKET_NAME",
    "R2_PUBLIC_URL",
)


def _get_env(name: str) -> str:
    """環境変数を取得。未設定なら ``RuntimeError``。"""
    v = os.environ.get(name, "").strip()
    if not v:
        raise RuntimeError(
            f"環境変数 {name} が未設定です。`.env` を確認してください。"
        )
    return v


def check_env() -> None:
    """R2 関連の環境変数がすべて揃っているか検査する。"""
    missing = [k for k in REQUIRED_ENVS if not os.environ.get(k)]
    if missing:
        raise RuntimeError(
            f"R2 環境変数が不足: {', '.join(missing)}。`.env` を確認してください。"
        )


def _build_client() -> Any:
    """boto3 の S3 クライアントを R2 エンドポイント向けに構築する。"""
    if boto3 is None:
        raise RuntimeError(
            "boto3 が未インストールです。"
            "`pip install -r scripts/requirements.txt` を実行してください。"
        )
    account_id = _get_env("R2_ACCOUNT_ID")
    return boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=_get_env("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=_get_env("R2_SECRET_ACCESS_KEY"),
        config=BotoConfig(signature_version="s3v4"),
        region_name="auto",
    )


def upload_image(
    src: Path,
    *,
    key_prefix: str = "instagram",
    dry_run: bool = False,
) -> str:
    """画像を R2 にアップロードし、公開 URL を返す。

    Args:
        src: アップロードするローカルファイル。
        key_prefix: バケット内のキーの先頭（フォルダ相当）。
        dry_run: True のとき実アップロードはせず、想定 URL のみ返す。

    Returns:
        公開 URL（``R2_PUBLIC_URL`` をベースに付与）。
    """
    if not src.exists():
        raise FileNotFoundError(f"画像ファイルが見つかりません: {src}")

    today = datetime.now().strftime("%Y%m%d")
    suffix = src.suffix.lower() or ".jpg"
    key = f"{key_prefix}/{today}/{uuid4().hex}{suffix}"
    public_base = os.environ.get("R2_PUBLIC_URL", "").rstrip("/")
    public_url = f"{public_base}/{key}" if public_base else f"r2://{key}"

    if dry_run:
        logger.info("[dry-run] R2 upload skipped: %s -> %s", src, public_url)
        return public_url

    check_env()
    client = _build_client()
    bucket = _get_env("R2_BUCKET_NAME")
    content_type, _ = mimetypes.guess_type(str(src))
    extra: dict[str, Any] = {}
    if content_type:
        extra["ContentType"] = content_type

    logger.info("R2 アップロード開始: %s -> s3://%s/%s", src, bucket, key)
    client.upload_file(str(src), bucket, key, ExtraArgs=extra)
    logger.info("R2 アップロード完了: %s", public_url)
    return public_url


def upload_if_local(path_or_url: str, *, dry_run: bool = False) -> str:
    """URL ならそのまま、ローカルパスなら R2 にアップロードして URL を返す。

    Args:
        path_or_url: ``http(s)://...`` または ローカルファイルパス。
        dry_run: dry-run モードか。

    Returns:
        投稿に使える公開 URL。
    """
    s = path_or_url.strip()
    if s.startswith(("http://", "https://")):
        return s
    return upload_image(Path(s).expanduser(), dry_run=dry_run)
