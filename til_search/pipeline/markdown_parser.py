import hashlib

from model.document import Document


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

    def _make_id(self, title: list[str], file_path: str):
        return hashlib.sha256((f"{"".join(title)}-{file_path}").encode()).hexdigest()
    
    def parse(self, base_path, file_path: str):
        def append_doc():
            parsed_result.append(Document(
                            id=self._make_id(title.values(), base_path),
                            title = list(title.values()),
                            content="\n".join(content),
                            path=base_path
                        ))
        
        with open(file_path, "r", encoding="utf8") as f:
            code_block = False
            lines = f.readlines()
        
        title = {}
        parsed_result = []
        content = []
        for line in lines:
            if line.lstrip().startswith("```"):
                code_block = not code_block
                continue
            if code_block:
                continue
            line = line.rstrip()
            if line.startswith("#"):
                if content:
                    append_doc()
                    content = []
                title = self._parse_title(line, title)
                
            else:
                if line:
                    content.append(line)
        if content:
            append_doc()
        
        return parsed_result