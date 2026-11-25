# extetagram-ios

Экспериментальный проект iOS-клиента. GitHub Actions собирает закреплённую версию Telegram-iOS. Функции exteraGram запланированы. **ChatLab Dev** — временное имя сборки для iPhone. [Исходный коммит Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS/commit/24638bc69bd083981b178dd1e7f921eebbf7fc46)

Независимый проект. Telegram-iOS распространяется под GNU GPL v2 или новее. Этот репозиторий содержит скрипт с изменениями, которые применяются к указанному коммиту при сборке. [Лицензия исходного клиента](https://telegram.org/apps#telegram-for-ios)

## Сборка и установка

1. В GitHub откройте **Actions → Build iPhone IPA for SideStore** и запустите workflow вручную.
2. После завершения скачайте ZIP из раздела **Artifacts** и извлеките файл `.ipa`.
3. Импортируйте `.ipa` в SideStore. SideStore подпишет и установит приложение на телефоне. [Документация SideStore](https://docs.sidestore.io/)

По умолчанию сборка не требует учётных данных Telegram API: она предназначена для проверки компиляции, установки и запуска. Войти в Telegram с ней нельзя. Расширения и фоновые push-уведомления в прототипе не поддерживаются.

Для сборки с входом в Telegram используйте приватный репозиторий. Добавьте собственные `TELEGRAM_API_ID` и `TELEGRAM_API_HASH` в **Settings → Secrets and variables → Actions**, затем включите `enable_telegram_login` при запуске workflow. Значения встраиваются в IPA. [Получение ключей Telegram](https://core.telegram.org/api/obtaining_api_id)
