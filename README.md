# extetagram-ios

Независимый клиент для iPhone на базе открытого Telegram-iOS, вдохновлённый exteraGram Lite. **ChatLab Dev** — временное имя приложения. GitHub Actions загружает закреплённую версию Telegram-iOS и применяет изменения из этого репозитория. [Исходники Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) · [exteraGram Lite](https://github.com/exteraSquad/exteraGram#editions) · [Лицензия Telegram-iOS](https://telegram.org/apps#telegram-for-ios)

## Статус

Настроена сборка для SideStore без локального Mac. Проверочный запуск прошёл подготовку и дошёл до компиляции. Установка на iPhone и вход в Telegram пока не проверены. [Проверочный запуск](https://github.com/shaurma228/extetagram-ios/actions/runs/45668836173)

## Сборка и установка

1. Открой **Actions → Build iPhone IPA for SideStore → Run workflow**. [Workflow на GitHub](https://github.com/shaurma228/extetagram-ios/actions/workflows/build-sidestore.yml)
2. После успешной сборки скачай архив `ChatLab-SideStore` из раздела **Artifacts** и извлеки `ChatLab-SideStore.ipa`.
3. На iPhone выбери IPA через **SideStore → My Apps → +**. SideStore подпишет и установит приложение. [Документация SideStore](https://docs.sidestore.io/)

Сборка по умолчанию предназначена для проверки установки и запуска. Для входа в Telegram собери приложение в приватной копии проекта со своими Telegram API-ключами. Ключи встраиваются в IPA. [Получение ключей](https://core.telegram.org/api/obtaining_api_id)

## Развитие проекта

[План реализации](PLAN.md)
