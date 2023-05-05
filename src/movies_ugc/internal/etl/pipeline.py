from dataclasses import dataclass

from movies_ugc.internal.etl.extractor import AsyncExtractor
from movies_ugc.internal.etl.loader import AsyncLoader
from movies_ugc.internal.etl.transformer import AsyncTransformer

TypeLoaders = tuple[AsyncLoader, ...]
TypeTransformerLoadersMapping = tuple[AsyncTransformer, TypeLoaders]


@dataclass(slots=True)
class AsyncETLPipeline:
    extractor: AsyncExtractor
    transformer_loaders_mapping: tuple[TypeTransformerLoadersMapping, ...]

    async def run(self):
        raw_data = self.extractor.extract()
        for tr, loaders in self.transformer_loaders_mapping:
            transformed_data = tr.transform(raw_data)
            for loader in loaders:
                await loader.load(transformed_data)
