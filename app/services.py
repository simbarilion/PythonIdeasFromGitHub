def process_repositories(
    query: str,
    repos: list,
):
    processed = [
        {
            "name": repo["name"],
            "owner": repo["owner"]["login"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
        }
        for repo in repos
    ]
    total_stars = sum(repo["stars"] for repo in repos)
    average_stars = total_stars / len(processed) if processed else 0
    top_repo = processed[0]["name"] if processed else None
    return {
        "query": query,
        "repos_count": len(processed),
        "total_stars": total_stars,
        "average_stars": round(average_stars, 2),
        "top_repo": top_repo,
        "repos": processed,
    }
