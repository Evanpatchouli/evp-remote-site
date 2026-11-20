import DefaultTheme from 'vitepress/theme'
import Home from './Home.vue'
import ClientDownload from './ClientDownload.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ProductHome', Home)
    app.component('ClientDownload', ClientDownload)
  }
}
