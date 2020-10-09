export { default as AlertMessage } from '../..\\components\\AlertMessage.vue'
export { default as Draggable } from '../..\\components\\Draggable.vue'
export { default as Header } from '../..\\components\\Header.vue'
export { default as MainPage } from '../..\\components\\MainPage.vue'
export { default as Modal } from '../..\\components\\Modal.vue'
export { default as SideMenu } from '../..\\components\\SideMenu.vue'

export const LazyAlertMessage = import('../..\\components\\AlertMessage.vue' /* webpackChunkName: "components_AlertMessage" */).then(c => c.default || c)
export const LazyDraggable = import('../..\\components\\Draggable.vue' /* webpackChunkName: "components_Draggable" */).then(c => c.default || c)
export const LazyHeader = import('../..\\components\\Header.vue' /* webpackChunkName: "components_Header" */).then(c => c.default || c)
export const LazyMainPage = import('../..\\components\\MainPage.vue' /* webpackChunkName: "components_MainPage" */).then(c => c.default || c)
export const LazyModal = import('../..\\components\\Modal.vue' /* webpackChunkName: "components_Modal" */).then(c => c.default || c)
export const LazySideMenu = import('../..\\components\\SideMenu.vue' /* webpackChunkName: "components_SideMenu" */).then(c => c.default || c)
