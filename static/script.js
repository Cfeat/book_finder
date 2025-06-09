document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    const isbnInput = document.getElementById('isbn-input');
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');
    const resultsContainer = document.getElementById('results-container');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const isbn = isbnInput.value.trim();
        if (!isbn) return;

        loader.style.display = 'block';
        errorMessage.style.display = 'none';
        resultsContainer.style.display = 'none';

        try {
            const response = await fetch(`/api/query?isbn=${encodeURIComponent(isbn)}`);
            const data = await response.json();

            if (!response.ok || !data.found) {
                throw new Error(data.message || '查询失败，请检查 ISBN 号码。');
            }

            displayBookInfo(data);

        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        } finally {
            loader.style.display = 'none';
        }
    });

    function displayBookInfo(data) {
        document.getElementById('book-title').textContent = data.title;
        document.getElementById('book-authors').textContent = data.authors;
        document.getElementById('book-publishers').textContent = data.publishers;
        document.getElementById('book-publish-date').textContent = data.publish_date;
        document.getElementById('book-pages').textContent = data.number_of_pages;

        const coverImg = document.getElementById('book-cover-img');
        if (data.cover_url) {
            coverImg.src = data.cover_url;
            coverImg.style.display = 'block';
        } else {
            coverImg.style.display = 'none'; 
        }

        const subjectsContainer = document.getElementById('book-subjects');
        const subjectsDiv = document.getElementById('book-subjects-container');
        subjectsContainer.innerHTML = '';
        if (data.subjects && data.subjects.length > 0) {
            data.subjects.forEach(subject => {
                const tag = document.createElement('span');
                tag.className = 'subject-tag';
                tag.textContent = subject;
                subjectsContainer.appendChild(tag);
            });
            subjectsDiv.style.display = 'block';
        } else {
            subjectsDiv.style.display = 'none';
        }

        resultsContainer.style.display = 'flex';
    }
});