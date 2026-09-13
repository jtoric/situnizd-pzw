import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    layout?: 'gost' | 'aplikacija'
    javno?: boolean
    uloga?: 'admin' | 'klub'
  }
}
