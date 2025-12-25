// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          // 主色系
          primary: '#2E7D32',        // 绿色
          secondary: '#1976D2',      // 蓝色
          accent: '#FF6F00',         // 橙色
          
          // 系统色
          success: '#4CAF50',
          warning: '#FFA726',
          error: '#EF5350',
          info: '#29B6F6',
          
          // 中性色
          background: '#FAFAFA',
          surface: '#FFFFFF',
          'surface-variant': '#F5F5F5',
          
          // 自定义
          'primary-light': '#A5D6A7',
          'primary-lighter': '#C8E6C9',
          'secondary-light': '#64B5F6',
          'secondary-lighter': '#BBDEFB',
          
          // 文本颜色
          'text-primary': '#212121',
          'text-secondary': '#757575',
          'text-disabled': '#BDBDBD'
        }
      }
    }
  },
  
  // 全局组件默认属性
  defaults: {
    // 卡片
    VCard: {
      elevation: 2,
      rounded: 'lg'
    },
    VBtn: {
      rounded: 'md',
      textTransform: 'none',
      fontWeight: 500
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
      hideDetails: 'auto'
    },
    VSelect: {
      variant: 'outlined',
      density: 'comfortable',
      hideDetails: 'auto'
    },
    VTextarea: {
      variant: 'outlined',
      density: 'comfortable'
    },
    VAppBar: {
      elevation: 4,
      rounded: 'md'
    },
    VChip: {
      rounded: 'md'
    }
  }
})
