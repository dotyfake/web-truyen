module.exports = function(eleventyConfig) {
    // Chỉ định thư mục input, includes và output
    eleventyConfig.addPassthroughCopy("css"); // Nếu bạn muốn có file CSS riêng

    // Tạo collection cho mỗi bộ truyện, sắp xếp theo số chương
    eleventyConfig.addCollection("truyen", function(collectionApi) {
        return collectionApi.getFilteredByGlob("truyen/**/*.md").sort((a, b) => {
            if (a.data.story < b.data.story) return -1;
            if (a.data.story > b.data.story) return 1;
            return a.data.chapterNumber - b.data.chapterNumber;
        });
    });

    // Pagination để tạo link chương trước/sau cho từng truyện
    eleventyConfig.addCollection("paginatedStories", function(collectionApi) {
        const stories = collectionApi.getFilteredByGlob("truyen/**/*.md");
        let paginatedStories = {};
        stories.forEach(story => {
            if (!paginatedStories[story.data.story]) {
                paginatedStories[story.data.story] = [];
            }
            paginatedStories[story.data.story].push(story);
        });

        for (const storyName in paginatedStories) {
            paginatedStories[storyName].sort((a, b) => a.data.chapterNumber - b.data.chapterNumber);
            paginatedStories[storyName].forEach((item, index, all) => {
                item.pagination = {
                    previous: all[index - 1],
                    next: all[index + 1]
                };
            });
        }
        return paginatedStories;
    });

    // Tạo collection chứa danh sách tên các truyện (không trùng lặp)
    eleventyConfig.addCollection("storyList", function(collectionApi) {
        let storySet = new Set();
        collectionApi.getFilteredByGlob("truyen/**/*.md").forEach(item => {
            storySet.add(item.data.story);
        });
        return [...storySet].sort();
    });

    return {
        dir: {
            input: ".",
            includes: "_includes",
            output: "_site",
            data: "_data"
        },
        markdownTemplateEngine: "njk",
        htmlTemplateEngine: "njk",
    };
};