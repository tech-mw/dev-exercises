FROM node:20

WORKDIR /usr/src/app

COPY package.json .

# 本番用は --only=production に切替
RUN npm install

# 依存インストール後コピー、キャッシュを最適化
COPY main.js .

# 起動コマンド
# package.json内のscriptsを利用
# - 開発時は "npm run dev"（ホットリロード有効）
# - 本番時は "npm run start"（ホットリロードなし）
CMD ["npm", "run", "dev"]