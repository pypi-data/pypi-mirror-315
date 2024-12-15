from parselite import parse, FastParser
from searchlite import google, bing
from wordllama import WordLlama

llm = WordLlama.load()


def vision(query,k=1,max_urls=5,animation=False):
    try:
        urls = google(query,max_urls=max_urls,animation=animation)
        contents = parse(urls)
        context = "".join(contents) + "\n\nURLS:\n" + "\n".join(urls)
        res = llm.topk(query, llm.split("".join(context)),k=k)
    except:
        return "Error Google Search query Not Found Results."
    return "\n".join(res)

def visionbing(query,k=1,max_urls=5,animation=False):
    try:
        urls = bing(query, max_urls=max_urls, animation=animation)
        contents = parse(urls)
        context = "".join(contents) + "\n\nURLS:\n" + "\n".join(urls)
        res = llm.topk(query, llm.split("".join(context)), k=k)
    except:
        return "Error Bing Search query Not Found Results."
    return "\n".join(res)

async def avision(query,k=1,max_urls=5,animation=False):
    try:
        urls = google(query,max_urls=max_urls,animation=animation)
        parser = FastParser()
        contents = await parser._async_html_parser(urls)
        context = "".join(contents) + "\n\nURLS:\n" + "\n".join(urls)
        res = llm.topk(query, llm.split("".join(context)),k=k)
    except:
        return "Error Google Search query Not Found Results."
    return "\n".join(res)
