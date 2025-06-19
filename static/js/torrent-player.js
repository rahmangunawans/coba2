class TorrentPlayer {
    constructor(videoElement, options = {}) {
        this.video = videoElement;
        this.client = null;
        this.torrent = null;
        this.options = {
            autoplay: true,
            playbackRate: 3,
            ...options
        };
        
        this.initializeWebTorrent();
    }
    
    initializeWebTorrent() {
        if (typeof WebTorrent === 'undefined') {
            console.error('WebTorrent not available');
            return false;
        }
        
        this.client = new WebTorrent({
            tracker: {
                rtcConfig: {
                    iceServers: [
                        { urls: 'stun:stun.l.google.com:19302' },
                        { urls: 'stun:global.stun.twilio.com:3478' }
                    ]
                }
            }
        });
        
        return true;
    }
    
    async loadMagnet(magnetUri) {
        return new Promise((resolve, reject) => {
            if (!this.client) {
                reject(new Error('WebTorrent client not initialized'));
                return;
            }
            
            console.log('Loading magnet:', magnetUri);
            
            // Prevent browser from trying to open external client
            const cleanMagnet = magnetUri.trim();
            
            this.client.add(cleanMagnet, (torrent) => {
                this.torrent = torrent;
                console.log('Torrent loaded:', torrent.name);
                
                // Find video file
                const videoFile = this.findVideoFile(torrent.files);
                
                if (videoFile) {
                    this.streamVideoFile(videoFile);
                    resolve(videoFile);
                } else {
                    reject(new Error('No video file found in torrent'));
                }
            });
            
            this.client.on('error', (err) => {
                console.error('WebTorrent error:', err);
                reject(err);
            });
        });
    }
    
    findVideoFile(files) {
        const videoExtensions = /\.(mp4|mkv|avi|mov|wmv|flv|webm|m4v|3gp|ogv)$/i;
        
        // Find video files larger than 50MB
        let videoFiles = files.filter(file => 
            videoExtensions.test(file.name) && file.length > 50 * 1024 * 1024
        );
        
        if (videoFiles.length === 0) {
            // Fallback to any video file
            videoFiles = files.filter(file => videoExtensions.test(file.name));
        }
        
        if (videoFiles.length === 0) {
            // Last resort - largest file
            return files.reduce((prev, current) => 
                (prev.length > current.length) ? prev : current
            );
        }
        
        // Return largest video file
        return videoFiles.reduce((prev, current) => 
            (prev.length > current.length) ? prev : current
        );
    }
    
    streamVideoFile(file) {
        console.log('Streaming file:', file.name);
        
        // Prevent browser from opening external torrent client
        event?.preventDefault?.();
        
        // Use renderTo for better browser compatibility
        file.renderTo(this.video, {
            autoplay: this.options.autoplay,
            muted: false,
            controls: false
        });
        
        // Set playback rate after video loads
        this.video.addEventListener('loadedmetadata', () => {
            this.video.playbackRate = this.options.playbackRate;
        });
        
        // Handle video events
        this.video.addEventListener('loadstart', () => {
            console.log('Video loading started');
        });
        
        this.video.addEventListener('canplay', () => {
            console.log('Video can start playing');
        });
    }
    
    getStats() {
        if (!this.torrent) return null;
        
        return {
            downloadSpeed: this.torrent.downloadSpeed,
            uploadSpeed: this.torrent.uploadSpeed,
            progress: this.torrent.progress,
            numPeers: this.torrent.numPeers,
            downloaded: this.torrent.downloaded,
            uploaded: this.torrent.uploaded,
            length: this.torrent.length
        };
    }
    
    destroy() {
        if (this.client) {
            this.client.destroy();
            this.client = null;
        }
        this.torrent = null;
    }
}

// Utility functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function isMagnetLink(url) {
    return url && url.trim().toLowerCase().startsWith('magnet:');
}

// Export for global use
window.TorrentPlayer = TorrentPlayer;
window.formatBytes = formatBytes;
window.isMagnetLink = isMagnetLink;