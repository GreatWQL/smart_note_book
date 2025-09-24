import { createI18n } from 'vue-i18n'
import zhCN from './locales/zh-CN.json'
import enUS from './locales/en-US.json'
import koKR from './locales/ko-KR.json'
import jaJP from './locales/ja-JP.json'
import frFR from './locales/fr-FR.json'

const messages = {
  'zh-CN': zhCN,
  'en-US': enUS,
  'ko-KR': koKR,
  'ja-JP': jaJP,
  'fr-FR': frFR
}

// 从localStorage获取保存的语言设置，默认为中文
const savedLocale = localStorage.getItem('locale') || 'zh-CN'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'zh-CN',
  messages
})

export default i18n