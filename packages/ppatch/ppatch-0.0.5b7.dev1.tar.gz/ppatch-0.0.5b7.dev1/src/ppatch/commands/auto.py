import os

import typer

from ppatch.app import app, logger
from ppatch.commands.get import getpatches
from ppatch.commands.trace import trace
from ppatch.config import settings
from ppatch.model import CommandResult, CommandType, Diff, File
from ppatch.utils.common import process_json_config, process_title
from ppatch.utils.parse import changes_to_hunks, parse_patch
from ppatch.utils.resolve import apply_change


@app.command()
def auto(
    filename: str,
    output: str = typer.Option("", "--output", "-o"),
    extra_config: str = typer.Option("", "--extra-config", "-c"),
):
    """Automatic do ANYTHING"""
    if not os.path.exists(filename):
        logger.error(f"{filename} not found!")

        return CommandResult(
            type=CommandType.AUTO,
        )

    if not os.path.exists(output) and not output.endswith(".patch"):
        logger.error(f"output {output} not found!")
        return CommandResult(
            type=CommandType.AUTO,
        )

    if os.path.isdir(output):
        output = os.path.join(output, "auto.patch")

    content = ""
    with open(filename, mode="r", encoding="utf-8") as (f):
        content = f.read()

    parser = parse_patch(content)
    fail_file_list: dict[str, list[int]] = {}
    diffes: list[Diff] = parser.diff
    for diff in diffes:
        target_file = diff.header.new_path  # 这里注意是 new_path 还是 old_path

        if not os.path.exists(target_file):
            logger.error(f"File {target_file} not found!")
            return CommandResult(
                type=CommandType.AUTO,
            )

        origin_file = File(file_path=target_file)

        # 执行 Reverse，确定失败的 Hunk
        apply_result = apply_change(
            diff.hunks, origin_file.line_list, reverse=True, fuzz=3
        )

        if len(apply_result.failed_hunk_list) != 0:
            logger.info(f"Failed hunk in {target_file}")
            fail_file_list[target_file] = [
                hunk.index for hunk in apply_result.failed_hunk_list
            ]

    if len(fail_file_list) == 0:
        logger.info("No failed patch")

        return CommandResult(
            type=CommandType.AUTO,
        )

    subject = parser.subject
    diffes: list = []
    for file_name, hunk_list in fail_file_list.items():
        logger.info(
            f"{len(hunk_list)} hunk(s) failed in {file_name} with subject {subject}"
        )

        hit_list, sha_list = getpatches(file_name, subject, save=True)
        sha_for_sure = None

        for sha in hit_list:
            with open(
                os.path.join(
                    settings.base_dir,
                    settings.patch_store_dir,
                    f"{sha}-{process_title(file_name)}.patch",
                ),
                mode="r",
                encoding="utf-8",
            ) as (f):
                text = f.read()

                # logger.debug(f"1st: {parse_patch(text).subject}")
                # logger.debug(f"2nd: {subject}")

                target_subject = parse_patch(text).subject
                if target_subject in subject or subject in target_subject:
                    sha_for_sure = sha
                    break

        if sha_for_sure is None:
            logger.error(f"No patch found for {file_name}")

            return CommandResult(
                type=CommandType.AUTO,
            )

        logger.info(f"Found correspond patch {sha_for_sure} to {file_name}")
        logger.info(f"Hunk list: {hunk_list}")

        symbols: list[str] = None
        if extra_config != "":
            logger.info(f"Using extra config {extra_config}")
            # with open(extra_config, mode="r", encoding="utf-8") as (extra_config_file):
            # extra_config_json: list | dict = json.load(extra_config_file)

            extra_config_json = process_json_config(extra_config)
            symbols = extra_config_json.get(file_name, None)

            logger.debug(f"Symbols to search in {file_name}: {symbols}")

        conflict_list = trace(
            sha_list,
            file_name,
            from_commit=sha_for_sure,
            flag_hunk_list=hunk_list,
            symbols=symbols,
        )

        line_list = File(file_path=file_name).line_list
        conflict_list = list(conflict_list.items())
        conflict_list.reverse()

        for sha, apply_result in conflict_list:
            # 对 apply_result.failed_hunk_list 中的冲突块按照 hunk.index 进行排序
            apply_result.failed_hunk_list = sorted(
                apply_result.failed_hunk_list, key=lambda x: x.index
            )

            logger.info(
                f"Conflict hunk in {sha}: {[hunk.index for hunk in apply_result.failed_hunk_list]}"
            )

            changes = []
            for hunk in apply_result.failed_hunk_list:
                changes.extend(hunk.all_)

            _apply_result = apply_change(
                changes_to_hunks(changes), line_list, reverse=True, fuzz=3
            )
            # TODO: 错误处理
            try:
                assert len(_apply_result.failed_hunk_list) == 0
            except AssertionError:
                logger.error(
                    f"AUTO: Failed hunk in {sha}; len: {len(_apply_result.failed_hunk_list)}"
                )

            line_list = _apply_result.new_line_list

        origin_file = File(file_path=file_name)
        patched_text = "\n".join([line.content for line in line_list])
        origin_text = "\n".join([line.content for line in origin_file.line_list])

        import difflib

        diffes_ = difflib.unified_diff(
            origin_text.splitlines(),
            patched_text.splitlines(),
            fromfile="a/" + file_name,
            tofile="b/" + file_name,
        )

        for line in diffes_:
            diffes.append(line + "\n" if not line.endswith("\n") else line)

    with open(
        output,
        mode="w+",
        encoding="utf-8",
    ) as (f):
        patch_content = "".join(diffes)
        if len(patch_content) == 0:
            logger.error("No patch generated")
            return CommandResult(
                type=CommandType.AUTO,
            )

        f.write(patch_content)
        logger.info(f"Patch file generated: {output}")

    return CommandResult(
        type=CommandType.AUTO,
    )
