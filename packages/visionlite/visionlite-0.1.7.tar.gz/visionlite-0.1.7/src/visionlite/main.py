from parselite import parse, FastParser
from searchlite import google, bing
from wordllama import WordLlama

llm = WordLlama.load()


def vision(query,k=1,max_urls=5,animation=False):
    try:
        urls = google(query,max_urls=max_urls,animation=animation)
        contents = parse(urls)
        res = llm.topk(query, llm.split("".join(contents)), k=k)
        updated_res = "\n".join(res) + "\n\nURLS:\n" + "\n".join(urls)
    except:
        return "Error Google Search query Not Found Results."
    return updated_res

def visionbing(query,k=1,max_urls=5,animation=False):
    try:
        urls = bing(query, max_urls=max_urls, animation=animation)
        contents = parse(urls)
        res = llm.topk(query, llm.split("".join(contents)), k=k)
        updated_res = "\n".join(res) + "\n\nURLS:\n" + "\n".join(urls)
    except:
        return "Error Google Search query Not Found Results."
    return updated_res


async def avision(query,k=1,max_urls=5,animation=False):
    try:
        urls = google(query,max_urls=max_urls,animation=animation)
        parser = FastParser()
        contents = await parser._async_html_parser(urls)
        res = llm.topk(query, llm.split("".join(contents)),k=k)
        updated_res = "\n".join(res) + "\n\nURLS:\n" + "\n".join(urls)
    except:
        return "Error Google Search query Not Found Results."
    return updated_res
