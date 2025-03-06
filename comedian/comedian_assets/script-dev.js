// Main controller for the comedian animation
class ComedianStage {
    constructor() {
        // Get DOM elements
        this.stage = document.getElementById('comedy-stage');
        this.curtainLeft = document.querySelector('.curtain-left');
        this.curtainRight = document.querySelector('.curtain-right');
        this.spotlight = document.querySelector('.spotlight');
        this.comedian = document.querySelector('.comedian');
        this.jokeBubble = document.querySelector('.joke-bubble');
        this.jokeText = document.getElementById('joke-text');
        
        // Animation containers
        this.animationContainers = {
            pacingRight: document.querySelector('.pacing-right'),
            pacingLeft: document.querySelector('.pacing-left'),
            talking: document.querySelector('.talking'),
            laughing: document.querySelector('.laughing')
        };
        
        // Individual states
        this.comedianStates = {
            entering: document.querySelector('.comedian-state.entering'),
            standing: document.querySelector('.comedian-state.standing'),
            thinking: document.querySelector('.comedian-state.thinking')
        };
        
        // Stage dimensions
        this.stageWidth = this.stage.offsetWidth;
        this.characterWidth = this.comedian.offsetWidth;
        
        // Animation frames for each container
        this.frames = {
            pacingRight: Array.from(document.querySelectorAll('.pacing-right .animation-frame')),
            pacingLeft: Array.from(document.querySelectorAll('.pacing-left .animation-frame')),
            talking: Array.from(document.querySelectorAll('.talking .animation-frame')),
            laughing: Array.from(document.querySelectorAll('.laughing .animation-frame'))
        };
        
        // Animation timers and state
        this.timers = [];
        this.currentState = 'entering';
        this.currentFrame = 0;
        this.frameInterval = null;
        
        // Pacing variables
        this.isPacing = false;
        this.pacingDirection = 'right';
        this.pacingPosition = 0;
        this.pacingSpeed = 3; // pixels per frame
        this.pacingAreaWidth = this.stageWidth * 0.7; // % of stage width to use for pacing
        
        // Pacing boundaries
        this.leftBoundary = this.stageWidth / 2 - this.pacingAreaWidth / 2;
        this.rightBoundary = this.stageWidth / 2 + this.pacingAreaWidth / 2;
        
        // Jokes
        this.jokes = [];
        this.currentJokeIndex = 0;
        this.isShowingPunchline = false;
        this.isJoking = false;
        
        // Animation speeds
        this.frameRate = 150; // ms between frames
        
        // Initialize
        this.init();
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    handleResize() {
        // Update stage dimensions on window resize
        this.stageWidth = this.stage.offsetWidth;
        this.pacingAreaWidth = this.stageWidth * 0.7;
        this.leftBoundary = this.stageWidth / 2 - this.pacingAreaWidth / 2;
        this.rightBoundary = this.stageWidth / 2 + this.pacingAreaWidth / 2;
    }
    
    async init() {
        // Load jokes from JSON file
        try {
            const response = await fetch('comedian_assets/dadJokes.json');
            this.jokes = await response.json();
            console.log('Jokes loaded:', this.jokes.length);
        } catch (error) {
            console.error('Error loading jokes:', error);
            // Fallback jokes in case the file doesn't load
            this.jokes = [
                {"joke": "Why don't scientists trust atoms?", "punchline": false},
                {"joke": "Because they make up everything!", "punchline": true},
                {"joke": "I'm reading a book on anti-gravity.", "punchline": false},
                {"joke": "It's impossible to put down!", "punchline": true}
            ];
        }
        
        // Start the show after a short delay
        setTimeout(() => this.startShow(), 1000);
    }
    
    startShow() {
        // 1. Open the curtain
        this.curtainLeft.classList.add('curtain-open');
        this.curtainRight.classList.add('curtain-open');
        
        // Audio effect for curtain
        this.playSoundEffect('curtain');
        
        // 2. After curtain opens, show comedian entering
        this.timers.push(setTimeout(() => {
            this.setState('entering');
            
            // 3. Move comedian to center stage
            this.timers.push(setTimeout(() => {
                this.comedian.classList.add('on-stage');
                this.playSoundEffect('footsteps');
                
                // 4. Turn on spotlight
                this.timers.push(setTimeout(() => {
                    this.spotlight.classList.add('spotlight-on');
                    this.playSoundEffect('spotlight');
                    
                    // 5. Comedian stands ready
                    this.timers.push(setTimeout(() => {
                        this.setState('standing');
                        
                        // 6. Start the comedy routine
                        this.timers.push(setTimeout(() => {
                            this.startComedyRoutine();
                        }, 1000));
                    }, 500));
                }, 800));
            }, 1000));
        }, 1500));
    }
    
    startComedyRoutine() {
        // Start with pacing behavior
        this.startPacing();
        
        // After a short period of pacing, start the jokes
        this.timers.push(setTimeout(() => {
            this.stopPacing();
            this.startJokeRoutine();
        }, 8000));
    }
    
    startPacing() {
        if (this.isPacing) return;
        
        this.isPacing = true;
        this.comedian.classList.add('pacing');
        
        // Initialize pacing variables
        this.pacingDirection = 'right';
        this.pacingPosition = this.leftBoundary;
        
        // Position comedian at the left boundary
        this.updateComedianPosition();
        
        // Set initial animation state
        this.setState('pacingRight');
        
        // Start frame animation
        this.startFrameAnimation();
        
        // Start movement animation
        this.animatePacing();
    }
    
    animatePacing() {
        if (!this.isPacing) return;
        
        // Move in current direction
        if (this.pacingDirection === 'right') {
            this.pacingPosition += this.pacingSpeed;
            
            // Check if reached right boundary
            if (this.pacingPosition >= this.rightBoundary) {
                this.pacingDirection = 'left';
                this.setState('pacingLeft');
            }
        } else {
            this.pacingPosition -= this.pacingSpeed;
            
            // Check if reached left boundary
            if (this.pacingPosition <= this.leftBoundary) {
                this.pacingDirection = 'right';
                this.setState('pacingRight');
            }
        }
        
        // Update position
        this.updateComedianPosition();
        
        // Occasionally show thinking pose
        if (Math.random() < 0.005) {
            const currentState = this.currentState;
            this.setState('thinking');
            
            // Return to pacing after a brief moment
            this.timers.push(setTimeout(() => {
                this.setState(currentState);
            }, 1000));
        }
        
        // Continue animation
        requestAnimationFrame(() => this.animatePacing());
    }
    
    updateComedianPosition() {
        // Calculate the actual screen position
        const positionPercent = (this.pacingPosition / this.stageWidth) * 100;
        this.comedian.style.left = `${positionPercent}%`;
        this.comedian.style.transform = 'translateX(-50%)';
    }
    
    stopPacing() {
        this.isPacing = false;
        this.comedian.classList.remove('pacing');
        
        // Return to center stage
        this.comedian.style.left = '50%';
        this.comedian.style.transform = 'translateX(-50%)';
        
        // Stop frame animation
        this.stopFrameAnimation();
        
        // Set standing state
        this.setState('standing');
    }
    
    startFrameAnimation() {
        // Already animating
        if (this.frameInterval) return;
        
        // Start cycling through frames
        this.frameInterval = setInterval(() => {
            this.animateNextFrame();
        }, this.frameRate);
    }
    
    animateNextFrame() {
        // Get frames array based on current state
        let framesArray;
        
        if (this.currentState === 'pacingRight') {
            framesArray = this.frames.pacingRight;
        } else if (this.currentState === 'pacingLeft') {
            framesArray = this.frames.pacingLeft;
        } else if (this.currentState === 'talking') {
            framesArray = this.frames.talking;
        } else if (this.currentState === 'laughing') {
            framesArray = this.frames.laughing;
        } else {
            // No frames to animate for other states
            return;
        }
        
        // Hide all frames
        framesArray.forEach(frame => {
            frame.classList.remove('active');
        });
        
        // Show next frame
        this.currentFrame = (this.currentFrame + 1) % framesArray.length;
        framesArray[this.currentFrame].classList.add('active');
    }
    
    stopFrameAnimation() {
        if (this.frameInterval) {
            clearInterval(this.frameInterval);
            this.frameInterval = null;
        }
        
        // Reset frame index
        this.currentFrame = 0;
    }
    
    startJokeRoutine() {
        this.isJoking = true;
        
        // Display the first joke
        this.displayNextJoke();
        
        // Setup the joke timing
        this.setupJokeTiming();
    }
    
    setupJokeTiming() {
        // Create a joke cycle
        this.jokeTimer = setInterval(() => {
            if (!this.isJoking) return;
            
            if (!this.isShowingPunchline) {
                this.displayPunchline();
            } else {
                // After punchline, decide what to do next
                if (Math.random() < 0.3) {
                    // 30% chance to pace between jokes
                    this.jokeBubble.classList.remove('active');
                    this.stopFrameAnimation();
                    this.startPacing();
                    
                    // Resume jokes after pacing
                    this.timers.push(setTimeout(() => {
                        this.stopPacing();
                        this.displayNextJoke();
                    }, 8000));
                } else {
                    // 70% chance to continue with next joke
                    this.displayNextJoke();
                }
            }
        }, 5000);
    }
    
    displayNextJoke() {
        // Find the next setup (non-punchline)
        let jokeIndex = this.currentJokeIndex;
        let foundJoke = false;
        
        while (!foundJoke) {
            if (!this.jokes[jokeIndex].punchline) {
                foundJoke = true;
                this.currentJokeIndex = jokeIndex;
            } else {
                jokeIndex = (jokeIndex + 1) % this.jokes.length;
            }
        }
        
        // Display the joke setup
        this.jokeText.textContent = this.jokes[this.currentJokeIndex].joke;
        this.jokeBubble.classList.add('active');
        this.setState('talking');
        this.isShowingPunchline = false;
        
        // Start frame animation if not already running
        this.startFrameAnimation();
        
        // Play voice sound effect
        this.playSoundEffect('voice');
        
        // Move to the next joke for next time (the punchline)
        this.currentJokeIndex = (this.currentJokeIndex + 1) % this.jokes.length;
    }
    
    displayPunchline() {
        // Find the punchline (should be right after the setup)
        if (this.jokes[this.currentJokeIndex].punchline) {
            this.jokeText.textContent = this.jokes[this.currentJokeIndex].joke;
            this.setState('laughing');
            this.isShowingPunchline = true;
            
            // Reset frame animation for laughing
            this.stopFrameAnimation();
            this.startFrameAnimation();
            
            // Play laugh sound effect
            this.playSoundEffect('laugh');
            
            // Move to the next joke for next time
            this.currentJokeIndex = (this.currentJokeIndex + 1) % this.jokes.length;
        } else {
            // If we somehow don't have a punchline, just go to the next joke
            this.displayNextJoke();
        }
    }
    
    setState(state) {
        // Skip if already in this state
        if (this.currentState === state) return;
        
        // Update current state
        this.currentState = state;
        
        // Hide all states and animation containers
        Object.values(this.comedianStates).forEach(el => {
            if (el) el.classList.remove('active');
        });
        
        Object.values(this.animationContainers).forEach(el => {
            if (el) el.classList.remove('active');
        });
        
        // Reset all animation frames
        Object.values(this.frames).forEach(framesArray => {
            framesArray.forEach(frame => {
                frame.classList.remove('active');
            });
        });
        
        // Show the requested state
        if (state === 'entering' || state === 'standing' || state === 'thinking') {
            // Simple states
            if (this.comedianStates[state]) {
                this.comedianStates[state].classList.add('active');
            }
        } else if (state === 'pacingRight' || state === 'pacingLeft' || state === 'talking' || state === 'laughing') {
            // Animation states
            const containerKey = state.replace('pacingRight', 'pacingRight').replace('pacingLeft', 'pacingLeft');
            
            if (this.animationContainers[containerKey]) {
                this.animationContainers[containerKey].classList.add('active');
                
                // Show first frame
                if (this.frames[containerKey] && this.frames[containerKey].length > 0) {
                    this.frames[containerKey][0].classList.add('active');
                }
            }
        }
    }
    
    playSoundEffect(type) {
        // This would be implemented to play actual sounds
        // For now just log the sound being played
        console.log(`Playing sound effect: ${type}`);
    }
    
    // Cleanup method for removing timers
    cleanup() {
        this.timers.forEach(timer => clearTimeout(timer));
        if (this.jokeTimer) clearInterval(this.jokeTimer);
        if (this.frameInterval) clearInterval(this.frameInterval);
        this.timers = [];
    }
}

// Wait for DOM to be loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the comedy stage
    const comedyStage = new ComedianStage();
    
    // Store the instance globally for debugging
    window.comedyStage = comedyStage;
});