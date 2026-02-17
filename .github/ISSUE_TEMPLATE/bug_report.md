---
name: 🐛 Bug Report
about: Something isn't working as expected
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ankit-chaubey
---

## 🐛 Bug Description

<!-- A clear and concise description of the bug. -->

## 📋 Steps to Reproduce

```rust
// Minimal code to reproduce the issue
use tgbotrs::Bot;

#[tokio::main]
async fn main() {
    let bot = Bot::new("TOKEN").await.unwrap();
    // ... steps that reproduce the bug
}
```

## 🤔 Expected Behavior

<!-- What you expected to happen. -->

## 😱 Actual Behavior

<!-- What actually happened. Include full error output. -->

```
error or panic output here
```

## 🌍 Environment

| | |
|---|---|
| **tgbotrs version** | `0.x.x` |
| **Rust version** | `rustc --version` output |
| **OS** | Ubuntu / Windows / macOS |
| **Telegram Bot API** | `9.x` |

## 📎 Additional Context

<!-- Any other context, screenshots, or logs. -->

## ✅ Checklist

- [ ] I searched for [existing issues](https://github.com/ankit-chaubey/tgbotrs/issues)
- [ ] I am using the latest version of tgbotrs
- [ ] I included a minimal reproducible example
