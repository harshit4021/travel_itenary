// JavaScript for AI Trip Planner Frontend

class TripPlannerApp {
    constructor() {
        this.baseURL = '';  // Since we're serving from the same domain
        this.currentTab = 'planner';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDestinations();
        this.loadTemplates();
        this.setMinDate();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Form submission
        document.getElementById('tripForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleTripFormSubmit();
        });

        // Date validation
        document.getElementById('startDate').addEventListener('change', () => {
            this.validateDates();
        });

        document.getElementById('endDate').addEventListener('change', () => {
            this.validateDates();
        });
    }

    setMinDate() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('startDate').min = today;
        document.getElementById('endDate').min = today;
    }

    validateDates() {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        if (startDate) {
            document.getElementById('endDate').min = startDate;
        }

        if (startDate && endDate && new Date(endDate) <= new Date(startDate)) {
            document.getElementById('endDate').value = '';
            this.showMessage('End date must be after start date', 'error');
        }
    }

    switchTab(tabName) {
        // Update nav tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;
    }

    async loadDestinations() {
        try {
            const response = await fetch('/destinations');
            const destinations = await response.json();
            this.renderDestinations(destinations);
        } catch (error) {
            console.error('Error loading destinations:', error);
        }
    }

    renderDestinations(destinations) {
        const container = document.getElementById('destinationsList');
        container.innerHTML = destinations.map(dest => `
            <div class="destination-card">
                <div class="destination-header">
                    <div class="destination-name">${dest.name}</div>
                    <div class="destination-country">${dest.country}</div>
                </div>
                <div class="destination-content">
                    <p class="destination-description">${dest.description}</p>
                    <div class="destination-tags">
                        ${dest.categories.map(cat => `<span class="tag">${cat}</span>`).join('')}
                    </div>
                    <div style="margin-top: 15px;">
                        <strong>Daily Budget:</strong>
                        <div style="margin-top: 5px;">
                            Budget: ₹${dest.avg_daily_budget.budget} | 
                            Mid: ₹${dest.avg_daily_budget.mid} | 
                            Luxury: ₹${dest.avg_daily_budget.luxury}
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #e1e8ed;">
                    <button class="btn-primary" onclick="app.initiateBooking(recommendation)" style="font-size: 1.2rem; padding: 15px 40px;">
                        <i class="fas fa-credit-card"></i> Book This Trip Now
                    </button>
                    <p style="margin-top: 10px; color: #666; font-size: 0.9rem;">
                        Secure booking with instant confirmation
                    </p>
                </div>
            </div>
        `).join('');
    }

    async loadTemplates() {
        try {
            const response = await fetch('/trip/templates');
            const templates = await response.json();
            this.renderTemplates(templates);
        } catch (error) {
            console.error('Error loading templates:', error);
        }
    }

    renderTemplates(templates) {
        const container = document.getElementById('templatesList');
        container.innerHTML = templates.map(template => `
            <div class="template-card">
                <div class="template-name">${template.name}</div>
                <p class="template-description">${template.description}</p>
                <div style="margin-bottom: 15px;">
                    <strong>Perfect for:</strong>
                    <div class="destination-tags" style="margin-top: 8px;">
                        ${template.preferences.interests.map(interest => 
                            `<span class="tag">${interest}</span>`
                        ).join('')}
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Destinations:</strong> ${template.recommended_destinations.map(dest => 
                        this.capitalizeFirst(dest.replace('_', ' '))
                    ).join(', ')}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Duration:</strong> ${template.duration_range[0]}-${template.duration_range[1]} days
                </div>
                ${template.highlights ? `
                    <div style="margin-bottom: 15px;">
                        <strong>Highlights:</strong> ${template.highlights.join(' • ')}
                    </div>
                ` : ''}
                <button class="btn-secondary" onclick="app.useTemplate('${template.name}')">
                    Use This Template
                </button>
            </div>
        `).join('');
    }

    async useTemplate(templateName) {
        try {
            const response = await fetch('/trip/templates');
            const templates = await response.json();
            const template = templates.find(t => t.name === templateName);
            
            if (template) {
                // Populate form with template data
                const preferences = template.preferences;
                
                // Set budget type
                document.getElementById('budgetType').value = preferences.budget_type;
                
                // Set travel style
                document.getElementById('travelStyle').value = preferences.travel_style;
                
                // Set accommodation type
                document.getElementById('accommodationType').value = preferences.accommodation_type;
                
                // Set activity intensity
                document.getElementById('activityIntensity').value = preferences.activity_intensity;
                
                // Set interests checkboxes
                document.querySelectorAll('input[name="interests"]').forEach(checkbox => {
                    checkbox.checked = preferences.interests.includes(checkbox.value);
                });
                
                // Set a recommended destination if available
                if (template.recommended_destinations && template.recommended_destinations.length > 0) {
                    document.getElementById('destination').value = template.recommended_destinations[0];
                }
                
                // Set default dates (next month for a week)
                const nextMonth = new Date();
                nextMonth.setMonth(nextMonth.getMonth() + 1);
                const startDate = nextMonth.toISOString().split('T')[0];
                
                const endDate = new Date(nextMonth);
                endDate.setDate(endDate.getDate() + template.duration_range[0]);
                const endDateStr = endDate.toISOString().split('T')[0];
                
                document.getElementById('startDate').value = startDate;
                document.getElementById('endDate').value = endDateStr;
                
                this.switchTab('planner');
                this.showMessage(`Template "${templateName}" applied! Adjust the details as needed.`, 'success');
                
                // Scroll to form
                document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
            }
        } catch (error) {
            console.error('Error applying template:', error);
            this.showMessage('Error applying template. Please try again.', 'error');
        }
    }

    async handleTripFormSubmit() {
        const formData = new FormData(document.getElementById('tripForm'));
        const tripRequest = this.buildTripRequest(formData);

        if (!this.validateTripRequest(tripRequest)) {
            return;
        }

        this.showLoading(true);

        try {
            console.log('Sending trip request:', tripRequest); // Debug log
            
            const response = await fetch('/trip/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tripRequest)
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server error:', errorText);
                throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
            }

            const recommendation = await response.json();
            console.log('Received recommendation:', recommendation); // Debug log
            this.displayTripRecommendation(recommendation);
            
        } catch (error) {
            console.error('Error planning trip:', error);
            this.showMessage(`Error planning your trip: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    buildTripRequest(formData) {
        const interests = Array.from(document.querySelectorAll('input[name="interests"]:checked'))
            .map(cb => cb.value);

        const request = {
            destination: formData.get('destination'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            travelers: parseInt(formData.get('travelers')) || 1,
            budget_total: formData.get('budget_total') ? parseFloat(formData.get('budget_total')) : null,
            preferences: {
                interests: interests,
                budget_type: formData.get('budget_type') || 'mid',
                travel_style: formData.get('travel_style') || 'cultural',
                accommodation_type: formData.get('accommodation_type') || 'mid',
                activity_intensity: formData.get('activity_intensity') || 'medium',
                dietary_restrictions: null,
                accessibility_needs: null,
                group_size_preference: "any"
            },
            special_requests: null
        };
        
        console.log('Built request:', request); // Debug log
        return request;
    }

    validateTripRequest(request) {
        if (!request.destination) {
            this.showMessage('Please select a destination', 'error');
            return false;
        }

        if (!request.start_date || !request.end_date) {
            this.showMessage('Please select both start and end dates', 'error');
            return false;
        }

        if (!request.preferences.interests || request.preferences.interests.length === 0) {
            this.showMessage('Please select at least one interest', 'error');
            return false;
        }

        return true;
    }

    displayTripRecommendation(recommendation) {
        console.log('Displaying recommendation:', recommendation); // Debug log
        
        // Store recommendation for booking
        this.currentRecommendation = recommendation;
        
        const resultsContainer = document.getElementById('tripResults');
        const resultsSection = document.getElementById('results');
        
        if (!resultsContainer) {
            console.error('tripResults element not found!');
            return;
        }
        
        try {
            resultsContainer.innerHTML = `
                <div class="results-header">
                    <h2><i class="fas fa-route"></i> Your Personalized Trip Plan</h2>
                    <div class="confidence-score">
                        <span>AI Confidence: ${Math.round(recommendation.confidence_score * 10)/10}/10</span>
                    </div>
                </div>

                ${this.renderTripOverview(recommendation)}
                ${this.renderItinerary(recommendation.trip.itinerary)}
                ${this.renderRecommendations(recommendation)}
            `;

            // Show the results section
            if (resultsSection) {
                resultsSection.style.display = 'block';
            }
            
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
            
            // Add event listener for booking button
            setTimeout(() => {
                const bookBtn = document.getElementById('bookTripBtn');
                if (bookBtn) {
                    bookBtn.addEventListener('click', () => {
                        this.initiateBooking(this.currentRecommendation);
                    });
                }
            }, 100);
            
        } catch (error) {
            console.error('Error rendering recommendation:', error);
            this.showMessage('Error displaying trip results. Please try again.', 'error');
        }
    }

    renderTripOverview(recommendation) {
        const trip = recommendation.trip;
        const duration = this.calculateDuration(trip.start_date, trip.end_date);
        
        return `
            <div class="trip-overview">
                <h3><i class="fas fa-map-marker-alt"></i> ${trip.destination}</h3>
                <p><strong>Travel Dates:</strong> ${this.formatDate(trip.start_date)} - ${this.formatDate(trip.end_date)}</p>
                <p><strong>Travelers:</strong> ${trip.travelers} person${trip.travelers > 1 ? 's' : ''}</p>
                
                <div class="trip-stats">
                    <div class="stat-item">
                        <span class="stat-value">${duration}</span>
                        <span class="stat-label">Days</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">₹${Math.round(recommendation.cost_breakdown.total)}</span>
                        <span class="stat-label">Total Cost</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">₹${Math.round(recommendation.cost_breakdown.per_person)}</span>
                        <span class="stat-label">Per Person</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${recommendation.confidence_score}/10</span>
                        <span class="stat-label">Confidence</span>
                    </div>
                </div>

                ${recommendation.personalization_notes.length > 0 ? `
                    <div style="margin-top: 20px;">
                        <strong>Personalization Notes:</strong>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            ${recommendation.personalization_notes.map(note => `<li>${note}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }

    renderWeatherInfo(weather) {
        return `
            <div class="weather-info">
                <h4><i class="fas fa-cloud-sun"></i> Weather Information</h4>
                <div class="weather-temp">${weather.temperature}°C</div>
                <div class="weather-condition">${this.capitalizeFirst(weather.condition)}</div>
                <div class="weather-recommendation">${weather.recommendation}</div>
            </div>
        `;
    }

    renderCostBreakdown(cost) {
        return `
            <div class="cost-breakdown">
                <h4><i class="fas fa-calculator"></i> Cost Breakdown</h4>
                <div class="cost-item">
                    <span>Accommodation</span>
                    <span>₹${Math.round(cost.accommodation)}</span>
                </div>
                <div class="cost-item">
                    <span>Activities</span>
                    <span>₹${Math.round(cost.activities)}</span>
                </div>
                <div class="cost-item">
                    <span>Food</span>
                    <span>₹${Math.round(cost.food)}</span>
                </div>
                <div class="cost-item">
                    <span>Transport</span>
                    <span>₹${Math.round(cost.transport)}</span>
                </div>
                <div class="cost-item">
                    <span><strong>Total</strong></span>
                    <span><strong>₹${Math.round(cost.total)}</strong></span>
                </div>
            </div>
        `;
    }

    renderItinerary(itinerary) {
        return `
            <div class="itinerary">
                <h4><i class="fas fa-calendar-alt"></i> Your Itinerary</h4>
                ${itinerary.map((day, index) => `
                    <div class="day-item">
                        <div class="day-header">
                            Day ${index + 1} - ${this.formatDate(day.date)}
                        </div>
                        <div class="day-content">
                            ${day.places && day.places.length > 0 ? 
                                day.places.map(place => `
                                    <div class="activity-item">
                                        <div class="activity-header">
                                            <span class="activity-name">
                                                <i class="fas fa-map-pin"></i> ${place.name}
                                            </span>
                                            <span class="activity-cost">₹${Math.round(place.cost_per_visitplace)}</span>
                                        </div>
                                        <div class="activity-description">
                                            ${place.description || ''}
                                        </div>
                                        <div style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                                            <i class="fas fa-clock"></i> ${place.times}
                                        </div>
                                        ${place.events && place.events.length > 0 ? `
                                            <div style="margin-top: 10px;">
                                                <strong>Activities:</strong>
                                                ${place.events.map(event => `
                                                    <div style="margin-left: 15px; margin-top: 5px;">
                                                        • ${event.name} (${event.time})
                                                    </div>
                                                `).join('')}
                                            </div>
                                        ` : ''}
                                    </div>
                                `).join('') 
                                : '<p>No specific activities planned for this day.</p>'
                            }
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderRecommendations(recommendation) {
        return `
            <div style="margin-top: 30px;">
                <h4><i class="fas fa-star"></i> Recommended Hotels</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 15px;">
                    ${recommendation.recommended_hotels.slice(0, 3).map(hotel => `
                        <div class="activity-item">
                            <div class="activity-header">
                                <span class="activity-name">${hotel.name}</span>
                                <span class="recommendation-score ${this.getScoreClass(hotel.recommendation_score?.overall_score)}">
                                    ${hotel.recommendation_score?.overall_score || 'N/A'}/10
                                </span>
                            </div>
                            <div class="activity-description">
                                ${hotel.description}
                            </div>
                            <div style="margin-top: 10px; font-size: 0.9rem;">
                                <strong>Location:</strong> ${hotel.location}<br>
                                <strong>Rating:</strong> ${hotel.rating}/5<br>
                                <strong>Amenities:</strong> ${hotel.amenities.join(', ')}
                            </div>
                        </div>
                    `).join('')}
                </div>

                <h4 style="margin-top: 30px;"><i class="fas fa-compass"></i> Recommended Activities</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 15px;">
                    ${recommendation.recommended_activities.slice(0, 6).map(activity => `
                        <div class="activity-item">
                            <div class="activity-header">
                                <span class="activity-name">${activity.name}</span>
                                <span class="recommendation-score ${this.getScoreClass(activity.recommendation_score?.overall_score)}">
                                    ${activity.recommendation_score?.overall_score || 'N/A'}/10
                                </span>
                            </div>
                            <div class="activity-description">
                                ${activity.description}
                            </div>
                            <div style="margin-top: 10px; font-size: 0.9rem;">
                                <strong>Duration:</strong> ${activity.duration}h<br>
                                <strong>Type:</strong> ${activity.type}<br>
                                <strong>Best Time:</strong> ${activity.best_time}<br>
                                <strong>Location:</strong> ${activity.location}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #e1e8ed;">
                <button class="btn-primary" id="bookTripBtn" style="font-size: 1.2rem; padding: 15px 40px;">
                    <i class="fas fa-credit-card"></i> Book This Trip Now
                </button>
                <p style="margin-top: 10px; color: #666; font-size: 0.9rem;">
                    Secure booking with instant confirmation
                </p>
            </div>
        `;
    }

    async initiateBooking(recommendation) {
        try {
            this.showLoading(true);
            
            const bookingRequest = {
                trip_id: `TRIP_${Date.now()}`,
                destination: recommendation.trip.destination,
                start_date: recommendation.trip.start_date,
                end_date: recommendation.trip.end_date,
                travelers: recommendation.trip.travelers,
                total_cost: recommendation.cost_breakdown.total,
                selected_hotel: recommendation.recommended_hotels[0]?.name,
                selected_activities: recommendation.recommended_activities.slice(0, 5).map(a => a.name)
            };

            const response = await fetch('/booking/initiate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookingRequest)
            });

            const bookingResponse = await response.json();
            this.showBookingPage(bookingResponse, recommendation);
            
        } catch (error) {
            console.error('Error initiating booking:', error);
            this.showMessage('Error initiating booking. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showBookingPage(bookingResponse, recommendation) {
        // Create booking page overlay
        const bookingOverlay = document.createElement('div');
        bookingOverlay.className = 'booking-overlay';
        bookingOverlay.innerHTML = `
            <div class="booking-page">
                <div class="booking-header">
                    <h2><i class="fas fa-plane"></i> Book Your Trip</h2>
                    <button class="close-booking" onclick="this.parentElement.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="booking-content">
                    <div class="prototype-notice">
                        <div class="prototype-badge">
                            <i class="fas fa-flask"></i> PROTOTYPE MODE
                        </div>
                        <h3>${bookingResponse.message}</h3>
                        <p>This is a demonstration of the booking system architecture. In production, this would integrate with real payment gateways and booking APIs.</p>
                    </div>

                    <div class="booking-summary">
                        <h3><i class="fas fa-receipt"></i> Booking Summary</h3>
                        <div class="summary-item">
                            <span>Destination:</span>
                            <span>${recommendation.trip.destination}</span>
                        </div>
                        <div class="summary-item">
                            <span>Duration:</span>
                            <span>${this.calculateDuration(recommendation.trip.start_date, recommendation.trip.end_date)} days</span>
                        </div>
                        <div class="summary-item">
                            <span>Travelers:</span>
                            <span>${recommendation.trip.travelers} person${recommendation.trip.travelers > 1 ? 's' : ''}</span>
                        </div>
                        <div class="summary-item">
                            <span>Booking ID:</span>
                            <span>${bookingResponse.details.booking_id}</span>
                        </div>
                        <div class="summary-item total">
                            <span>Total Amount:</span>
                            <span>₹${Math.round(bookingResponse.details.total_amount).toLocaleString()}</span>
                        </div>
                    </div>

                    <div class="development-roadmap">
                        <h3><i class="fas fa-road"></i> Development Roadmap</h3>
                        <div class="roadmap-phase">
                            <h4>Phase 1: Core Platform ✅</h4>
                            <ul>
                                <li>✅ AI-powered trip recommendations</li>
                                <li>✅ Budget optimization algorithms</li>
                                <li>✅ User preference matching</li>
                                <li>✅ Interactive frontend interface</li>
                            </ul>
                        </div>
                        
                        <div class="roadmap-phase">
                            <h4>Phase 2: Booking Integration 🚧</h4>
                            <ul>
                                ${bookingResponse.details.next_steps.map(step => `<li>🔄 ${step}</li>`).join('')}
                            </ul>
                        </div>

                        <div class="roadmap-phase">
                            <h4>Phase 3: Advanced Features 📋</h4>
                            <ul>
                                <li>📋 Real-time availability checking</li>
                                <li>📋 Multi-language support</li>
                                <li>📋 Mobile app development</li>
                                <li>📋 Social sharing features</li>
                            </ul>
                        </div>
                    </div>

                    <div class="demo-features">
                        <h3><i class="fas fa-star"></i> Planned Features</h3>
                        <div class="features-grid">
                            <div class="feature-item">
                                <i class="fas fa-credit-card"></i>
                                <h4>Payment Methods</h4>
                                <p>${bookingResponse.demo_features.payment_methods.join(', ')}</p>
                            </div>
                            <div class="feature-item">
                                <i class="fas fa-bell"></i>
                                <h4>Notifications</h4>
                                <p>${bookingResponse.demo_features.booking_confirmation}</p>
                            </div>
                            <div class="feature-item">
                                <i class="fas fa-undo"></i>
                                <h4>Cancellation</h4>
                                <p>${bookingResponse.demo_features.cancellation_policy}</p>
                            </div>
                            <div class="feature-item">
                                <i class="fas fa-headset"></i>
                                <h4>Support</h4>
                                <p>${bookingResponse.demo_features.customer_support}</p>
                            </div>
                        </div>
                    </div>

                    <div class="prototype-actions">
                        <button class="btn-primary" onclick="app.showMessage('This is a prototype! In production, this would process the actual payment.', 'success'); this.parentElement.parentElement.parentElement.parentElement.remove();">
                            <i class="fas fa-play"></i> Simulate Booking Process
                        </button>
                        <button class="btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">
                            <i class="fas fa-arrow-left"></i> Back to Trip Details
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(bookingOverlay);
    }

    getScoreClass(score) {
        if (!score) return '';
        if (score >= 8) return 'score-excellent';
        if (score >= 6) return 'score-good';
        return 'score-fair';
    }

    calculateDuration(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffTime = Math.abs(end - start);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'short', 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).replace('_', ' ');
    }

    showLoading(show) {
        document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());

        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;

        // Insert at the top of the form section
        const formSection = document.querySelector('.form-section');
        formSection.insertBefore(messageDiv, formSection.firstChild);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TripPlannerApp();
});
