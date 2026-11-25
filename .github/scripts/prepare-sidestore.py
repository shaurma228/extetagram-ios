"""Prepare the pinned Telegram-iOS checkout for a single-app SideStore build."""

import json
import os
from pathlib import Path


def replace_once(source: str, before: str, after: str) -> str:
    if source.count(before) != 1:
        raise SystemExit(f"Telegram-iOS source changed near {before.strip().splitlines()[0]!r}")
    return source.replace(before, after, 1)


app_delegate = Path("submodules/TelegramUI/Sources/AppDelegate.swift")
source = app_delegate.read_text()
source = replace_once(source, '''        let baseAppBundleId = Bundle.main.bundleIdentifier!
        let appGroupName = "group.\\(baseAppBundleId)"

        let configuration = URLSessionConfiguration.background(withIdentifier: identifier)
        configuration.sharedContainerIdentifier = appGroupName
''', '''        let configuration = URLSessionConfiguration.background(withIdentifier: identifier)
''')
source = replace_once(source, 'biometricKeychainService: walletBiometricKeychainService), privateAccessGroup: {',
                      'biometricKeychainService: walletBiometricKeychainService, usesSharedAppGroup: false), privateAccessGroup: {')
source = replace_once(source, '        let maybeAppGroupUrl = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: appGroupName)\n', '')
source = replace_once(source, '''        guard let appGroupUrl = maybeAppGroupUrl else {
            self.mainWindow?.presentNative(UIAlertController(title: nil, message: "Error 2", preferredStyle: .alert))
''', '''        guard let appGroupUrl = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask).first else {
            self.mainWindow?.presentNative(UIAlertController(title: nil, message: "Application storage unavailable", preferredStyle: .alert))
''')
app_delegate.write_text(source)

passcode = Path("submodules/PasscodeCore/Sources/Passcode.swift")
source = passcode.read_text()
source = replace_once(source, '''    public let keychainScope: String?

    public init(appGroupIdentifier: String, processRole: ProcessRole, biometricKeychainService: String? = nil, keychainScope: String? = nil) {
''', '''    public let keychainScope: String?
    public let usesSharedAppGroup: Bool

    public init(appGroupIdentifier: String, processRole: ProcessRole, biometricKeychainService: String? = nil, keychainScope: String? = nil, usesSharedAppGroup: Bool = true) {
''')
source = replace_once(source, '        self.keychainScope = keychainScope\n',
                      '        self.keychainScope = keychainScope\n        self.usesSharedAppGroup = usesSharedAppGroup\n')
source = replace_once(source, '''    public func sharedAccessGroup() throws -> String {
        self.mutex.lock()
        defer { self.mutex.unlock() }
        guard let configuration = self.configuration else { throw PasscodeError.unavailable }
        return configuration.appGroupIdentifier
    }
''', '''    public func sharedAccessGroup() throws -> String {
        self.mutex.lock()
        let configuration = self.configuration
        self.mutex.unlock()
        guard let configuration else { throw PasscodeError.unavailable }
        if !configuration.usesSharedAppGroup {
            return try self.privateAccessGroup()
        }
        return configuration.appGroupIdentifier
    }
''')
passcode.write_text(source)

build_file = Path("Telegram/BUILD")
source = build_file.read_text()
source = replace_once(source, '''    <key>CFBundleDisplayName</key>
    <string>Telegram</string>
    <key>CFBundleIdentifier</key>
''', '''    <key>CFBundleDisplayName</key>
    <string>ChatLab Dev</string>
    <key>CFBundleIdentifier</key>
''')
profile_default = '        "//conditions:default": ":Telegram_xcode_profile" if telegram_use_xcode_managed_codesigning else "@build_configuration//provisioning:Telegram.mobileprovision",\n    }),\n'
source = replace_once(source, profile_default + '    entitlements = ":TelegramEntitlements.entitlements",\n', profile_default)
source = replace_once(source, '''    app_icons = [ ":{}_icon".format(name) for name in composer_icon_folders ],
    alternate_icons = [
        ":{}".format(name) for name in alternate_icon_folders
    ],
''', '''    app_icons = glob(["Telegram-iOS/ChatLab.xcassets/ChatLab.appiconset/*"]),
''')
build_file.write_text(source)

config = json.loads(Path("build-system/template_minimal_development_configuration.json").read_text())
enable_login = os.environ["ENABLE_TELEGRAM_LOGIN"] == "true"
config.update(
    bundle_id=os.environ["APP_BUNDLE_ID"],
    api_id=os.environ["TELEGRAM_API_ID"] if enable_login else "0",
    api_hash=os.environ["TELEGRAM_API_HASH"] if enable_login else "0" * 32,
    # Bazel's template needs a team ID. SideStore supplies the real one at signing time.
    team_id="0000000000",
    is_internal_build="false",
    app_specific_url_scheme="chatlabdev",
)
config_path = Path(os.environ["RUNNER_TEMP"]) / "telegram-sidestore.json"
config_fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(config_fd, "w") as config_file:
    json.dump(config, config_file)
