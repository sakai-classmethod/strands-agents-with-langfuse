# Strands Agents with Langfuse

Strands AgentsとLangfuseを統合したAWS Knowledge Agentのサンプルプロジェクト。

## セットアップ手順

### 1. プロジェクトのセットアップ

リポジトリをクローンして依存関係をインストール:

```bash
git clone https://github.com/sakai-classmethod/strands-agents-with-langfuse
cd strands-agents-with-langfuse
uv sync
```

### 2. Langfuseのローカル起動

Docker Composeを使用してLangfuseをローカル環境で起動:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
```

起動後、ブラウザで `http://localhost:3000` にアクセスしてアカウントとプロジェクトを作成します。

### 3. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、必要な認証情報を設定:

```bash
# AWS認証情報
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key

# Langfuse認証情報
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxx
LANGFUSE_HOST=http://localhost:3000
```

※ Langfuseの認証情報はダッシュボードから取得できます

### 4. エージェントの実行

質問を引数として渡してエージェントを実行:

```bash
uv run python agent.py "S3バケットの命名規則について教えてください"
```

実行後、Langfuseのダッシュボード (`http://localhost:3000`) でトレース情報を確認できます。
