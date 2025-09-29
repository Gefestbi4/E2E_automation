// Social Module
console.log('📱 SocialModule script loading...');

class SocialModule {
    constructor() {
        this.posts = [];
        this.currentUser = null;
        this.init();
    }

    init() {
        console.log('📱 SocialModule initialized');
        this.loadPosts();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Event listeners for social features
        document.addEventListener('DOMContentLoaded', () => {
            const createPostBtn = document.getElementById('create-post-btn');
            if (createPostBtn) {
                createPostBtn.addEventListener('click', () => this.showCreatePostModal());
            }
        });
    }

    async loadPosts() {
        try {
            console.log('📱 Loading posts...');
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 100));
            this.posts = [
                { id: 1, content: 'Welcome to the social network!', author: 'System', likes: 0 },
                { id: 2, content: 'This is a test post', author: 'User', likes: 5 }
            ];
            this.renderPosts();
        } catch (error) {
            console.error('Error loading posts:', error);
        }
    }

    renderPosts() {
        const postsContainer = document.getElementById('posts-container');
        if (!postsContainer) return;

        postsContainer.innerHTML = this.posts.map(post => `
            <div class="post-card">
                <h3>${post.author}</h3>
                <p>${post.content}</p>
                <div class="post-actions">
                    <button onclick="SocialModule.likePost(${post.id})">👍 ${post.likes}</button>
                    <button onclick="SocialModule.commentOnPost(${post.id})">💬 Comment</button>
                </div>
            </div>
        `).join('');
    }

    showCreatePostModal() {
        console.log('📱 Showing create post modal');
        // Create modal for new post
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Create New Post</h2>
                <form id="create-post-form">
                    <textarea id="post-content" placeholder="What's on your mind?"></textarea>
                    <button type="submit">Post</button>
                </form>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'block';

        // Handle form submission
        document.getElementById('create-post-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const content = document.getElementById('post-content').value;
            if (content.trim()) {
                this.createPost(content);
                modal.remove();
            }
        });

        // Close modal
        modal.querySelector('.close').addEventListener('click', () => {
            modal.remove();
        });
    }

    async createPost(content) {
        try {
            const newPost = {
                id: Date.now(),
                content: content,
                author: 'Current User',
                likes: 0
            };
            this.posts.unshift(newPost);
            this.renderPosts();
            console.log('📱 Post created:', newPost);
        } catch (error) {
            console.error('Error creating post:', error);
        }
    }

    likePost(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
            post.likes++;
            this.renderPosts();
            console.log('📱 Post liked:', postId);
        }
    }

    commentOnPost(postId) {
        console.log('📱 Commenting on post:', postId);
        // Implement comment functionality
    }
}

// Export for global access
window.SocialModule = SocialModule;
console.log('📱 SocialModule class exported to window:', typeof window.SocialModule);
