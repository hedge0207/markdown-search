class MarkdownParser:
    
    def _parse_title(self, text: str, title: dict):
        depth = ""
        for i in range(len(text)):
            char = text[i]
            if char != "#":
                break
            depth += char
        title[depth] =text[len(depth)+1:]
        depth += "#"
        while title.get(depth):
            del title[depth]
            depth += "#"
        return title
    
    def parse(self, path: str):
        title = {}
        parsed_result = []
        with open(path, "r", encoding="utf8") as f:
            content = []
            code_block = False
            for line in f.readlines():
                if line.lstrip().startswith("```"):
                    code_block = not code_block
                    continue
                if code_block:
                    continue
                line = line.rstrip()
                if line.startswith("#"):
                    if content:
                        parsed_result.append({
                            "title": list(title.values()),
                            "content": "\n".join(content)
                        })
                        content = []
                    title = self._parse_title(line, title)
                else:
                    if line:
                        content.append(line)
            if content:
                parsed_result.append({
                    "title": list(title.values()),
                    "content": "\n".join(content)
                })
        
        return parsed_result