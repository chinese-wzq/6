function toggleSideMenu() {
    const sideMenu = document.getElementById("side-menu");
    const overlay = document.getElementById("overlay");
    sideMenu.classList.toggle("show");
    overlay.classList.toggle("show");
}

document.getElementById("overlay").addEventListener("click", toggleSideMenu);

let bridge = null;

window.onload = function() {
    if (typeof qt !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            bridge = channel.objects.bridge;
            console.log(bridge ? "Bridge连接成功" : "Bridge连接失败");
        });
    } else {
        console.log("qt对象未定义");
    }
}

function handleSend() {
    const input = document.querySelector('.input-field');
    const message = input.value.trim();
    if (!message) return;

    const chatArea = document.querySelector('.chat-area');
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.textContent = message;
    chatArea.appendChild(userMsg);

    // 添加加载动画
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    loadingDots.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    chatArea.appendChild(loadingDots);

    const model = document.querySelector('.model-dropdown').value;
    input.value = '';
    
    if (bridge && typeof bridge.handle_message === 'function') {
        bridge.handle_message(message, model).catch(function(error) {
            loadingDots.remove();
            console.error('调用 handle_message 时出错:', error);
            const errorMsg = document.createElement('div');
            errorMsg.className = 'message error';
            errorMsg.textContent = "发送消息时出错，请检查与后端的连接";
            chatArea.appendChild(errorMsg);
        });
    } else {
        loadingDots.remove();
        console.error("bridge对象未定义或handle_message方法不存在");
        const errorMsg = document.createElement('div');
        errorMsg.className = 'message error';
        errorMsg.textContent = "未能连接到后端服务";
        chatArea.appendChild(errorMsg);
    }
}

function receiveResponse(model, message) {
    // 移除等待动画
    const loadingDots = document.querySelector('.loading-dots');
    if (loadingDots) {
        loadingDots.remove();
    }
    
    // 创建新消息
    const aiMsg = document.createElement('div');
    aiMsg.className = 'message ai';
    
    // 设置消息内容
    try {
        // 使用 showdown 替代 marked
        if (window.showdown) {
            const converter = new showdown.Converter();
            aiMsg.innerHTML = converter.makeHtml(message);
        } else {
            aiMsg.textContent = message;
        }
    } catch (error) {
        console.error('Markdown parsing failed:', error);
        aiMsg.textContent = message;
    }
    
    // 添加到正确的容器
    const chatArea = document.querySelector('.chat-area');
    chatArea.appendChild(aiMsg);
    
    // 滚动到底部
    chatArea.scrollTop = chatArea.scrollHeight;
}