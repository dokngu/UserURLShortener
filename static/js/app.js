new Vue({
            el: '#app',
            data: {
                serviceURL: "https://cs3103.cs.unb.ca:8043",
                isAuthenticated: false,
                showLoginForm: false,
                showRegisterForm: false,
                loginData: {
                    username: '',
                    password: ''
                },
                registerData: {
                    username: '',
                    password: '',
                    email: ''
                },
                longUrl: '',
                shortUrl: ''
            },
            methods: {
                // Handle Login
                login() {
                    console.log(this.isAuthenticated);
                    axios.post(this.serviceURL+'/login', {
                        username: this.loginData.username,
                        password: this.loginData.password
                    })
                    .then(response => {
                        console.log(response)
                        if (response.status === 200) {
                            this.isAuthenticated = true;
                            this.showLoginForm = false;
                            this.showRegisterForm = false;
                            this.loginData = { username: '', password: '' };
                            alert('Login successful.');
                        }
                    })
                    .catch(error => {
                        if(error.response.status === 401) {
                            console.error('401 - Unauthorized');
                            alert('Invalid credentials.');
                        } else {
                            console.error('There was an error during login: ', error);
                            alert('An error occurred during login.');
                        }
                    });
                },
                
                register() {
                    console.log(this.isAuthenticated);
                    axios.post(this.serviceURL+'/users/new', {
                        username: this.registerData.username,
                        password: this.registerData.password,
                        email: this.registerData.email
                    })
                    .then(response => {
                        console.log(response)
                        this.showRegisterForm = false;
                        this.loginData = { username: '', password: '' };
                        this.registerData = { username: '', password: '', email: '' };
                        alert('Registration successful.');

                    })
                    .catch(error => {
                        console.error('There was an error during registration: ', error);
                        alert('An error occurred during registration.');
                    })
                },
                
                // Handle Logout
                logout() {
                    axios.post(this.serviceURL+'/logout')
                        .then(response => {
                            this.isAuthenticated = false;
                            this.shortUrl = ''; // Clear shortened URL
                            alert('Logout successful.');
                        })
                        .catch(error => {
                            console.error('There was an error during logout:', error);
                        });
                },
 
                // Handle URL Shortening
                shortenUrl() {
                    if (!this.longUrl) {
                        alert("Please enter a URL.");
                        return;
                    }
 
                    axios.post(this.serviceURL+'/urls', {
                        long_url: this.longUrl
                    })
                    .then(response => {
                        this.shortUrl = response.data.link;
                        console.log('short url is' + this.shortUrl);
                    })
                    .catch(error => {
                        console.error('Error shortening URL:', error);
                        alert('An error occurred while shortening the URL.');
                    });
                }
            }
        });
