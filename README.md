<div align="center">

<img src="https://raw.githubusercontent.com/rust-lang/www.rust-lang.org/master/static/images/ferris/rustacean-orig-noshadow.svg" width="120" alt="Ferris the Crab"/>

<h1>tgbotrs</h1>

<p><strong>A fully-featured, auto-generated Telegram Bot API library for Rust 🦀</strong></p>

[![Crates.io](https://img.shields.io/crates/v/tgbotrs?style=for-the-badge&logo=rust&color=f74c00&labelColor=1a1a2e)](https://crates.io/crates/tgbotrs)
[![docs.rs](https://img.shields.io/docsrs/tgbotrs?style=for-the-badge&logo=docs.rs&color=4a90d9&labelColor=1a1a2e)](https://docs.rs/tgbotrs)
[![CI](https://img.shields.io/github/actions/workflow/status/ankit-chaubey/tgbotrs/ci.yml?branch=main&style=for-the-badge&logo=github-actions&label=CI&color=2ea44f&labelColor=1a1a2e)](https://github.com/ankit-chaubey/tgbotrs/actions/workflows/ci.yml)
[![Auto-Regen](https://img.shields.io/github/actions/workflow/status/ankit-chaubey/tgbotrs/auto-regenerate.yml?style=for-the-badge&logo=telegram&label=API+SYNC&color=0088cc&labelColor=1a1a2e)](https://github.com/ankit-chaubey/tgbotrs/actions/workflows/auto-regenerate.yml)

[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-9.4-0088cc?style=for-the-badge&logo=telegram&logoColor=white&labelColor=1a1a2e)](https://core.telegram.org/bots/api)
[![Rust](https://img.shields.io/badge/Rust-1.75%2B-f74c00?style=for-the-badge&logo=rust&logoColor=white&labelColor=1a1a2e)](https://www.rust-lang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&labelColor=1a1a2e)](LICENSE)
[![Crates.io Downloads](https://img.shields.io/crates/d/tgbotrs?style=for-the-badge&color=ff6b6b&labelColor=1a1a2e&label=Downloads)](https://crates.io/crates/tgbotrs)

[![Types](https://img.shields.io/badge/Types-285-blueviolet?style=flat-square)](https://docs.rs/tgbotrs)
[![Methods](https://img.shields.io/badge/Methods-165-success?style=flat-square)](https://docs.rs/tgbotrs)
[![Coverage](https://img.shields.io/badge/API%20Coverage-100%25-brightgreen?style=flat-square)](https://github.com/ankit-chaubey/tgbotrs/actions)
[![Async](https://img.shields.io/badge/Async-Tokio-orange?style=flat-square)](https://tokio.rs)
[![Serde](https://img.shields.io/badge/Serde-JSON-lightgrey?style=flat-square)](https://serde.rs)

<br/>

> **All 285 types and 165 methods** of the Telegram Bot API — strongly typed, fully async, automatically kept up-to-date.

<br/>

[📦 Install](#-installation) • [🚀 Quick Start](#-quick-start) • [📖 Examples](#-examples) • [🔧 API Reference](#-api-reference) • [🔄 Auto-Codegen](#-auto-codegen) • [🤝 Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td>

**🤖 Complete API Coverage**
- All **285 types** — structs, enums, markers
- All **165 methods** — fully async
- All **21 union types** as Rust enums
- **100 optional params structs** with builder pattern

</td>
<td>

**🔄 Auto-Generated & Always Fresh**
- Generated from the [official spec](https://github.com/ankit-chaubey/api-spec)
- Daily automated check for API updates
- PR auto-opened on every new API version
- Zero manual work to stay up-to-date

</td>
</tr>
<tr>
<td>

**🦀 Idiomatic Rust**
- Fully `async/await` with **Tokio**
- `Into<ChatId>` — accepts `i64` or `"@username"`
- `Into<String>` on all text params
- `Option<T>` for all optional fields
- `Box<T>` to break recursive type cycles

</td>
<td>

**🛡️ Type Safe**
- `ChatId` — integer or username, no stringly typing
- `InputFile` — file_id / URL / raw bytes
- `ReplyMarkup` — unified enum for all 4 keyboard types
- `InputMedia` — typed enum for media groups
- Compile-time guarantees on all API calls

</td>
</tr>
<tr>
<td>

**📡 Flexible HTTP Layer**
- Custom API server support (local Bot API)
- Multipart file uploads
- Configurable timeout
- Flood-wait aware error handling
- `reqwest` backend

</td>
<td>

**📬 Built-in Polling**
- Long-polling dispatcher included
- Spawns a Tokio task per update
- Configurable timeout, limit, allowed_updates
- Clean concurrent update processing

</td>
</tr>
</table>

---

## 📦 Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
tgbotrs = "0.1"
tokio   = { version = "1", features = ["full"] }
```

**Requirements:** Rust `1.75+` · Tokio async runtime

---

## 🚀 Quick Start

```rust
use tgbotrs::Bot;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let bot = Bot::new("YOUR_BOT_TOKEN").await?;

    println!("✅ Running as @{}", bot.me.username.as_deref().unwrap_or("unknown"));
    println!("   ID: {}", bot.me.id);

    // Send a message — chat_id accepts i64 or "@username"
    let msg = bot.send_message(123456789i64, "Hello from tgbotrs! 🦀", None).await?;
    println!("📨 Sent message #{}", msg.message_id);

    Ok(())
}
```

---

## 📖 Examples

### 🔁 Echo Bot — Long Polling

```rust
use tgbotrs::{Bot, Poller, UpdateHandler};

#[tokio::main]
async fn main() {
    let bot = Bot::new(std::env::var("BOT_TOKEN").unwrap())
        .await.expect("Invalid token");

    println!("🤖 @{} is running...", bot.me.username.as_deref().unwrap_or(""));

    let handler: UpdateHandler = Box::new(|bot, update| {
        Box::pin(async move {
            let Some(msg) = update.message else { return };
            let Some(text) = msg.text else { return };
            let _ = bot.send_message(msg.chat.id, text, None).await;
        })
    });

    Poller::new(bot, handler).timeout(30).limit(100).start().await.unwrap();
}
```

---

### 💬 Formatted Messages

```rust
use tgbotrs::gen_methods::SendMessageParams;

let params = SendMessageParams::new()
    .parse_mode("HTML".to_string())
    .disable_notification(true);

bot.send_message(
    "@mychannel",
    "<b>Bold</b>, <i>italic</i>, <code>code</code>",
    Some(params),
).await?;
```

---

### 🎹 Inline Keyboards

```rust
use tgbotrs::{ReplyMarkup, gen_methods::SendMessageParams};
use tgbotrs::types::{InlineKeyboardMarkup, InlineKeyboardButton};

let keyboard = InlineKeyboardMarkup {
    inline_keyboard: vec![
        vec![
            InlineKeyboardButton { text: "✅ Accept".into(),  callback_data: Some("accept".into()),  ..Default::default() },
            InlineKeyboardButton { text: "❌ Decline".into(), callback_data: Some("decline".into()), ..Default::default() },
        ],
        vec![
            InlineKeyboardButton { text: "🌐 Visit".into(), url: Some("https://example.com".into()), ..Default::default() },
        ],
    ],
};

let params = SendMessageParams::new()
    .reply_markup(ReplyMarkup::InlineKeyboard(keyboard));

bot.send_message(chat_id, "Choose an option:", Some(params)).await?;
```

---

### 📸 Send Photos

```rust
use tgbotrs::{InputFile, gen_methods::SendPhotoParams};

let params = SendPhotoParams::new().caption("Nice photo! 📷".to_string());

// By file_id (fastest — already on Telegram's servers)
bot.send_photo(chat_id, "AgACAgIAAxkBAAI...", Some(params.clone())).await?;

// By URL
bot.send_photo(chat_id, "https://example.com/photo.jpg", Some(params.clone())).await?;

// Upload raw bytes
let data = tokio::fs::read("photo.jpg").await?;
bot.send_photo(chat_id, InputFile::memory("photo.jpg", data), Some(params)).await?;
```

---

### 🎬 Media Groups

```rust
use tgbotrs::{InputMedia};
use tgbotrs::types::{InputMediaPhoto, InputMediaVideo};

let media = vec![
    InputMedia::Photo(InputMediaPhoto {
        r#type: "photo".into(),
        media: "AgACAgIAAxkBAAI...".into(),
        caption: Some("First photo 📸".into()),
        ..Default::default()
    }),
    InputMedia::Video(InputMediaVideo {
        r#type: "video".into(),
        media: "BAACAgIAAxkBAAI...".into(),
        caption: Some("A video 🎬".into()),
        ..Default::default()
    }),
];

bot.send_media_group(chat_id, media, None).await?;
```

---

### ⌨️ Reply Keyboards

```rust
use tgbotrs::{ReplyMarkup, gen_methods::SendMessageParams};
use tgbotrs::types::{ReplyKeyboardMarkup, KeyboardButton};

let keyboard = ReplyKeyboardMarkup {
    keyboard: vec![
        vec![
            KeyboardButton { text: "📍 Location".into(), request_location: Some(true), ..Default::default() },
            KeyboardButton { text: "📱 Contact".into(),  request_contact: Some(true),  ..Default::default() },
        ],
    ],
    resize_keyboard: Some(true),
    one_time_keyboard: Some(true),
    ..Default::default()
};

let params = SendMessageParams::new()
    .reply_markup(ReplyMarkup::ReplyKeyboard(keyboard));

bot.send_message(chat_id, "Use the keyboard below:", Some(params)).await?;
```

---

### 📊 Polls

```rust
use tgbotrs::{gen_methods::SendPollParams};
use tgbotrs::types::InputPollOption;

let options = vec![
    InputPollOption { text: "🦀 Rust".into(),   ..Default::default() },
    InputPollOption { text: "🐹 Go".into(),     ..Default::default() },
    InputPollOption { text: "🐍 Python".into(), ..Default::default() },
];

let params = SendPollParams::new().is_anonymous(false);

bot.send_poll(chat_id, "Best language for bots?", options, Some(params)).await?;
```

---

### ⚡ Callback Queries

```rust
use tgbotrs::gen_methods::AnswerCallbackQueryParams;
use tgbotrs::types::MaybeInaccessibleMessage;

let handler: UpdateHandler = Box::new(|bot, update| {
    Box::pin(async move {
        let Some(cq) = update.callback_query else { return };
        let data = cq.data.as_deref().unwrap_or("");

        // Dismiss the loading spinner
        let _ = bot.answer_callback_query(
            cq.id.clone(),
            Some(AnswerCallbackQueryParams::new()
                .text(format!("You chose: {}", data))
                .show_alert(false)),
        ).await;

        // Edit original message
        if let Some(MaybeInaccessibleMessage::Message(m)) = cq.message {
            let _ = bot.edit_message_text(
                m.chat.id, m.message_id,
                format!("✅ Selected: <b>{}</b>", data),
                Some(tgbotrs::gen_methods::EditMessageTextParams::new()
                    .parse_mode("HTML".to_string())),
            ).await;
        }
    })
});
```

---

### 🏪 Inline Queries

```rust
use tgbotrs::types::{InlineQueryResult, InlineQueryResultArticle, InputMessageContent, InputTextMessageContent};

let results = vec![
    InlineQueryResult::Article(InlineQueryResultArticle {
        r#type: "article".into(),
        id: "1".into(),
        title: "Hello World".into(),
        input_message_content: InputMessageContent::Text(InputTextMessageContent {
            message_text: "Hello from inline mode! 👋".into(),
            ..Default::default()
        }),
        description: Some("Send a greeting".into()),
        ..Default::default()
    }),
];

bot.answer_inline_query(query.id.clone(), results, None).await?;
```

---

### 🛒 Payments

```rust
use tgbotrs::{gen_methods::SendInvoiceParams};
use tgbotrs::types::LabeledPrice;

let prices = vec![
    LabeledPrice { label: "Premium Plan".into(), amount: 999 },
];

bot.send_invoice(
    chat_id,
    "Premium Access",
    "30 days of unlimited features",
    "payload_premium_30d",
    "XTR",   // Telegram Stars
    prices,
    None,
).await?;
```

---

### 🔔 Webhooks

```rust
use tgbotrs::gen_methods::SetWebhookParams;

let params = SetWebhookParams::new()
    .max_connections(100i64)
    .allowed_updates(vec!["message".into(), "callback_query".into()])
    .secret_token("my_secret_token".to_string());

bot.set_webhook("https://mybot.example.com/webhook", Some(params)).await?;
```

---

### 🌐 Local Bot API Server

```rust
let bot = Bot::with_api_url("YOUR_TOKEN", "http://localhost:8081").await?;
```

---

### 🛠️ Error Handling

```rust
use tgbotrs::BotError;

match bot.send_message(chat_id, "Hello!", None).await {
    Ok(msg) => println!("✅ Sent: #{}", msg.message_id),

    Err(BotError::Api { code: 403, .. }) => {
        eprintln!("🚫 Bot was blocked by the user");
    }
    Err(BotError::Api { code: 400, description, .. }) => {
        eprintln!("⚠️  Bad request: {}", description);
    }
    Err(e) if e.is_api_error_code(429) => {
        if let Some(secs) = e.flood_wait_seconds() {
            println!("⏳ Flood wait: {} seconds", secs);
            tokio::time::sleep(std::time::Duration::from_secs(secs as u64)).await;
        }
    }
    Err(e) => eprintln!("❌ Error: {}", e),
}
```

---

## 🔧 API Reference

### `Bot` — Core Struct

```rust
pub struct Bot {
    pub token:   String,  // Bot token from @BotFather
    pub me:      User,    // Populated via getMe on creation
    pub api_url: String,  // API base URL (default: api.telegram.org)
}
```

| Constructor | Description |
|---|---|
| `Bot::new(token)` | Create bot, calls getMe, verifies token |
| `Bot::with_api_url(token, url)` | Create with a custom/local API server |
| `Bot::new_unverified(token)` | Create without calling getMe |

| Method | Description |
|---|---|
| `bot.call_api(method, body)` | Raw JSON POST API call |
| `bot.call_api_multipart(method, form)` | Multipart POST (for file uploads) |
| `bot.endpoint(method)` | Returns full URL for a method |

---

### `ChatId` — Flexible Chat Identifier

```rust
// All of these work wherever ChatId is expected:
bot.send_message(123456789i64,    "by integer id", None).await?;
bot.send_message(-100123456789i64, "group/channel", None).await?;
bot.send_message("@channelname",  "by username",   None).await?;
bot.send_message(ChatId::Id(123), "explicit",      None).await?;
```

---

### `InputFile` — File Sending

```rust
// Reference an already-uploaded file by file_id
InputFile::file_id("AgACAgIAAxkBAAI...")

// Let Telegram download from a URL
InputFile::url("https://example.com/image.png")

// Upload raw bytes directly
let data = tokio::fs::read("photo.jpg").await?;
InputFile::memory("photo.jpg", data)
```

---

### `ReplyMarkup` — All Keyboard Types

```rust
// Inline keyboard (buttons inside messages)
ReplyMarkup::InlineKeyboard(InlineKeyboardMarkup { .. })

// Reply keyboard (custom keyboard at bottom of screen)
ReplyMarkup::ReplyKeyboard(ReplyKeyboardMarkup { .. })

// Remove the reply keyboard
ReplyMarkup::ReplyKeyboardRemove(ReplyKeyboardRemove { remove_keyboard: true, .. })

// Force the user to reply
ReplyMarkup::ForceReply(ForceReply { force_reply: true, .. })
```

---

### `Poller` — Long Polling Dispatcher

```rust
Poller::new(bot, handler)
    .timeout(30)                                // Seconds to long-poll (0 = short poll)
    .limit(100)                                 // Max updates per request (1-100)
    .allowed_updates(vec![                      // Only receive these update types
        "message".into(),
        "callback_query".into(),
        "inline_query".into(),
        "chosen_inline_result".into(),
        "shipping_query".into(),
        "pre_checkout_query".into(),
    ])
    .start()
    .await?;
```

---

### `BotError` — Error Handling

```rust
pub enum BotError {
    Http(reqwest::Error),   // Network or HTTP transport error
    Json(serde_json::Error),// Serialization/deserialization error
    Api {
        code: i64,                      // Telegram error code (e.g. 400, 403, 429)
        description: String,            // Human-readable error message
        retry_after: Option<i64>,       // Seconds to wait (flood-wait, code 429)
        migrate_to_chat_id: Option<i64>,// New chat ID (migration error, code 400)
    },
    InvalidToken,           // Token does not contain ':'
    Other(String),          // Catch-all
}

// Helper methods:
error.is_api_error_code(429)  // → bool
error.flood_wait_seconds()    // → Option<i64>
```

---

### Builder Pattern for Optional Params

Every method with optional parameters has a `*Params` struct with a builder API:

```rust
// Pattern: MethodNameParams::new().field(value).field(value)
let params = SendMessageParams::new()
    .parse_mode("MarkdownV2".to_string())
    .disable_notification(true)
    .protect_content(false)
    .message_thread_id(123i64)
    .reply_parameters(ReplyParameters { message_id: 42, ..Default::default() })
    .reply_markup(ReplyMarkup::ForceReply(ForceReply {
        force_reply: true, ..Default::default()
    }));
```

---

## 📊 Coverage Statistics

| Category | Count | Status |
|---|:---:|:---:|
| **Total Types** | **285** | ✅ 100% |
| ↳ Struct types | 257 | ✅ |
| ↳ Union/Enum types | 21 | ✅ |
| ↳ Marker types | 7 | ✅ |
| **Total Methods** | **165** | ✅ 100% |
| ↳ `set*` methods | 30 | ✅ |
| ↳ `get*` methods | 29 | ✅ |
| ↳ `send*` methods | 22 | ✅ |
| ↳ `edit*` methods | 12 | ✅ |
| ↳ `delete*` methods | 11 | ✅ |
| ↳ Other methods | 61 | ✅ |
| **Params structs** | 100 | ✅ |
| **Lines generated** | ~11,258 | — |

---

## 🔄 Auto-Codegen

tgbotrs is the only Rust Telegram library that **automatically stays in sync** with the official API spec via GitHub Actions.

### Architecture

```
Every Day at 08:00 UTC
        │
        ▼
  ┌─────────────────┐
  │  Fetch latest   │  ←── github.com/ankit-chaubey/api-spec
  │  api.json spec  │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Compare with   │── No change? ──► Stop ✅
  │  pinned version │
  └────────┬────────┘
           │ Changed!
           ▼
  ┌─────────────────┐
  │  diff_spec.py   │  ←── Full semantic diff
  │                 │       • Added/removed types
  │                 │       • Added/removed methods
  │                 │       • Per-field changes
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  codegen.py     │  ←── Pure Python, zero dependencies
  │                 │       Generates:
  │                 │       • gen_types.rs  (5,821 lines)
  │                 │       • gen_methods.rs (5,437 lines)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  validate.py    │  ←── Verify 100% coverage
  │                 │       All types & methods present
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Open PR with   │  ←── Rich description:
  │  full report    │       • Summary table
  │                 │       • New/removed items
  │                 │       • Per-field diff (collapsible)
  │                 │       • Checklist
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  GitHub Issue   │  ←── Notification with full changelog
  │  notification   │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  On PR merge:   │
  │  • Bump semver  │
  │  • Git tag      │
  │  • GitHub Release│
  │  • crates.io    │
  └─────────────────┘
```

### Regenerate Manually

```sh
# 1. Download latest spec
curl -o api.json \
  https://raw.githubusercontent.com/ankit-chaubey/api-spec/main/api.json

# 2. Run codegen (pure Python, no pip installs needed)
python3 codegen/codegen.py api.json tgbotrs/src/

# 3. Rebuild your project
cargo build
```

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `auto-regenerate.yml` | ⏰ Daily 08:00 UTC + manual | Fetch spec → diff → codegen → PR |
| `ci.yml` | Every push/PR | Build, test, lint, validate sync |
| `release.yml` | PR merged → main | Version bump + crates.io publish |
| `notify.yml` | After regen | GitHub Issue with change summary |

### Setting Up in Your Fork

Add these secrets in **Settings → Secrets → Actions**:

| Secret | Purpose |
|---|---|
| `CRATES_IO_TOKEN` | API token from [crates.io/settings/tokens](https://crates.io/settings/tokens) |

Enable PR creation in **Settings → Actions → General → Workflow permissions**.

---

## 🏗️ Project Structure

```
tgbotrs/
│
├── 📄 README.md                 ← You are here
├── 📄 CHANGELOG.md              ← Auto-updated on each release
├── 📄 LICENSE                   ← MIT — Ankit Chaubey 2024-present
├── 📄 api.json                  ← Pinned Telegram Bot API spec
├── 📄 spec_commit               ← Pinned spec commit SHA
├── 📄 Cargo.toml                ← Workspace root
│
├── 🗂️  .github/
│   ├── workflows/
│   │   ├── auto-regenerate.yml  ← Daily spec sync + codegen + PR opener
│   │   ├── ci.yml               ← Build/test on 3 OSes × 2 Rust versions
│   │   ├── release.yml          ← Semver bump + tag + publish
│   │   └── notify.yml           ← Issue creation on API updates
│   └── scripts/
│       ├── diff_spec.py         ← Semantic diff: added/removed/changed
│       ├── validate_generated.py← Verifies 100% type + method coverage
│       ├── build_pr_body.py     ← Generates rich PR descriptions
│       ├── coverage_report.py   ← Markdown coverage table for CI
│       └── update_changelog.py  ← Auto-prepends entries to CHANGELOG.md
│
├── 🗂️  codegen/
│   ├── Cargo.toml
│   ├── codegen.py               ← Main codegen: Python, zero deps
│   └── src/main.rs              ← Rust codegen binary (alternative)
│
└── 🗂️  tgbotrs/                 ← The library crate
    ├── Cargo.toml
    ├── examples/
    │   ├── echo_bot.rs          ← Basic echo bot
    │   └── advanced_bot.rs      ← Keyboards, photos, callbacks
    └── src/
        ├── lib.rs               ← Crate root + public API + re-exports
        ├── bot.rs               ← Bot struct + HTTP + JSON API layer
        ├── error.rs             ← BotError with all error variants
        ├── chat_id.rs           ← ChatId (i64 | @username)
        ├── input_file.rs        ← InputFile + InputFileOrString
        ├── reply_markup.rs      ← ReplyMarkup (4-variant enum)
        ├── polling.rs           ← Poller (long-polling dispatcher)
        ├── types.rs             ← Re-exports gen_types
        ├── gen_types.rs         ← ⚡ AUTO-GENERATED — 5,821 lines
        └── gen_methods.rs       ← ⚡ AUTO-GENERATED — 5,437 lines
```

---

## 🤝 Contributing

Contributions are very welcome!

### Report Issues

- 🐛 **Bug?** → [Open a bug report](https://github.com/ankit-chaubey/tgbotrs/issues/new?template=bug_report.md)
- 💡 **Feature request?** → [Open a feature request](https://github.com/ankit-chaubey/tgbotrs/issues/new?template=feature_request.md)
- 🔒 **Security issue?** → Email [ankitchaubey.dev@gmail.com](mailto:ankitchaubey.dev@gmail.com) directly

### Development

```sh
# Clone the repo
git clone https://github.com/ankit-chaubey/tgbotrs
cd tgbotrs

# Build everything
cargo build --workspace

# Run tests
cargo test --workspace

# Regenerate from latest spec
python3 codegen/codegen.py api.json tgbotrs/src/

# Validate 100% coverage
python3 .github/scripts/validate_generated.py \
  api.json \
  tgbotrs/src/gen_types.rs \
  tgbotrs/src/gen_methods.rs

# Lint
cargo clippy --workspace --all-targets -- -D warnings

# Format
cargo fmt --all
```

### PR Guidelines

- One concern per PR
- Run `cargo fmt` and `cargo clippy` before submitting
- Add examples for new helpers
- Keep generated files (`gen_*.rs`) untouched — edit `codegen.py` instead

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

---

## 🙏 Credits

| | |
|---|---|
| **[Telegram](https://core.telegram.org/bots/api)** | The official Bot API this library implements |
| **[PaulSonOfLars / gotgbot](https://github.com/PaulSonOfLars/gotgbot)** | Design inspiration for the auto-generation approach and code structure |
| **[ankit-chaubey / api-spec](https://github.com/ankit-chaubey/api-spec)** | Machine-readable Telegram Bot API spec used as the codegen source |

---

## 📬 Contact

<div align="center">

| | |
|:---:|:---:|
| 📧 **Email** | [ankitchaubey.dev@gmail.com](mailto:ankitchaubey.dev@gmail.com) |
| 💬 **Telegram** | [@ankify](https://t.me/ankify) |
| 🐙 **GitHub** | [github.com/ankit-chaubey](https://github.com/ankit-chaubey) |
| 📦 **crates.io** | [crates.io/crates/tgbotrs](https://crates.io/crates/tgbotrs) |
| 📖 **docs.rs** | [docs.rs/tgbotrs](https://docs.rs/tgbotrs) |

</div>

---

## 📄 License

```
MIT License

Copyright (c) 2024-present Ankit Chaubey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

<div align="center">

**Created and developed by [Ankit Chaubey](https://github.com/ankit-chaubey)**

*If tgbotrs saved you time, a ⭐ on GitHub means a lot!*

<br/>

[![GitHub stars](https://img.shields.io/github/stars/ankit-chaubey/tgbotrs?style=social)](https://github.com/ankit-chaubey/tgbotrs/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ankit-chaubey/tgbotrs?style=social)](https://github.com/ankit-chaubey/tgbotrs/network/members)
[![Telegram](https://img.shields.io/badge/Telegram-@ankify-0088cc?style=social&logo=telegram)](https://t.me/ankify)

</div>
