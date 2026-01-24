# team-i-sns

## Quick Start(動かす)
### 1. Clone
```bash
git clone <REPO_URL> #初回のみ、以降はgit pull
cd team-i-sns

### 2. env
cp .env.example .env

### 3. docker
docker compose up
docker compose ps

access: http:://localhost:55000/login

docker compose stop
docker compose down

### 4.  Git branch
main:提出用（直接push禁止）
develop:統合先（常に最新）
feature/<topic> :作業用→PR→developへ

例: feature-login-ui

#作業手順
```bash
git checkout(or switch) develop
git pull origin develop
git checkout -b(or siwtch -c) fearture/xxx

git add .(or fail name)
git commit -m "feat: xxx"
git push -u origin feature/xxx

PR feature → develop
title: feat: xxx

type	意味
feat	新機能
fix	バグ修正
style	見た目のみ（CSSなど）
refactor	振る舞いを変えない整理
docs	READMEなど文書
chore	環境・設定・雑務

git branch -d feature/xxx #merge済みの場合の削除方法
git branch -D feature/xxx #強制削除
git push origin --delete feature/xxx #remote buranchの削除方法


