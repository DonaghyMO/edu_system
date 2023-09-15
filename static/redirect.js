// redirect.js

// 使用 window.onload 事件绑定方法，确保在页面加载完成后执行
window.onload = function() {
    clearPageAndRedirect();
};

function clearPageAndRedirect() {
    // 清空页面内容
    document.body.innerHTML = '';

    // 实现跳转
    window.location.href = "https://www.baidu.com";
}
