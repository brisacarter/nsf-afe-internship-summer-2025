
        let currentSlideIndex = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;

        document.getElementById('totalSlides').textContent = totalSlides;

         function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
            
            const slideNumber = index + 1;
            const formattedSlideNumber = slideNumber < 10 ? '0' + slideNumber : slideNumber;
            document.getElementById('currentSlide').textContent = formattedSlideNumber;
            
            document.getElementById('prevBtn').disabled = index === 0;
            document.getElementById('nextBtn').disabled = index === totalSlides - 1;
        }
        function changeSlide(direction) {
            const newIndex = currentSlideIndex + direction;
            if (newIndex >= 0 && newIndex < totalSlides) {
                currentSlideIndex = newIndex;
                showSlide(currentSlideIndex);
            }
        }

        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowRight' || event.key === ' ') {
                changeSlide(1);
            } else if (event.key === 'ArrowLeft') {
                changeSlide(-1);
            }
        });

        // Initialize
        showSlide(0);
