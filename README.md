# team-i-sns

## Quick Start(動かす)
### 1. Clone
```bash
git clone <REPO_URL>
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
git pull
git checkout -b(or siwtch -c) fearture/xxx

git add .(or fail name)
git commit -m "feat: xxx"
git push -u origin feature/xxx

PR → develop
title: feat: or fix:

