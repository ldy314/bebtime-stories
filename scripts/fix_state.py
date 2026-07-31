#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_state.py — 将 dangdang-series-state.json 同步到「全部 ep01-19 胎教期、真实生成于 2026-07-31」的状态。
以 automation 目录的副本为权威，改完后再整体同步到其余 3 份，避免副本漂移。
- lastGeneratedDate -> 2026-07-31
- arc.startedEpisode -> 9（奇妙朋友从 ep09 茅山遇修猴子开启）
- continuity[8]  (ep09) -> 茅山遇修猴子（胎教期，讲给肚里宝宝）
- continuity[9]  (ep10) -> 讲给宝宝听（胎教期）
- continuity[10] (ep11) -> 胎教期（宝宝还在肚里）
- continuity[18] (ep19) -> 胎教期（想象给肚里宝宝表演）
"""
import json
import os
import shutil

CANON = "C:/Users/Administrator/WorkBuddy/automation-2026-07-16-11-56-46/dangdang-series-state.json"
OTHER = [
    "D:/code test/睡前故事/dangdang-series-state.json",
    "D:/code test/睡前故事/github-pages/dangdang-series-state.json",
    "D:/code test/睡前故事/storyline/00-权威源文件/dangdang-series-state.json",
]

NEW_CONT9 = ("第9集《茅山遇修猴子》：一家人赴常州近郊仙山茅山，山顶老桃树下遇见会温和小法术的修猴子——"
             "教当当让桃叶轻轻飘、和南南开玩笑、把格格巫看呆的彩虹；修猴子丢下『老友粉在广西等你们』伏笔，"
             "为日后广西之旅埋线。全篇是当当讲给肚里还没来的宝宝听的冒险，胎教期口吻。")
NEW_CONT10 = ("第10集《茅山的小猴子（当当讲给宝宝听）》：以『当当讲给肚里弟弟听的故事』重述茅山遇修猴子，"
              "保留修猴子与『老友粉在广西等你们』伏笔；胎教期口吻（哥哥给肚里弟弟讲故事）。")
NEW_CONT11 = ("第11集《广西遇老友粉》：兑现ep10『老友粉在广西等你们』伏笔，一家赴广西雨林，"
              "大象老友粉用长鼻子摘水果、吸水浇花，讲雨林故事，带出广西米粉与热带水果；"
              "胎教期口吻（宝宝还在妈妈肚里）。")
NEW_CONT19 = ("第19集《当当的小法术升级》：承接ep09修猴子所教飘叶，当当的小法术从飘半寸升级到飘一尺，"
              "想象给肚里的小宝宝表演逗笑；『奇妙朋友』阶段收束，回扣『本事用来制造快乐』。")
NEW_ARC_DESC = ("承接ep09修猴子所教飘叶（茅山遇修猴子），当当的小法术从飘半寸升级到飘一尺，"
                "想象给肚里的小宝宝表演逗笑；『奇妙朋友』阶段收束，回扣本事用来制造快乐。")


def main():
    with open(CANON, "r", encoding="utf-8") as f:
        st = json.load(f)
    st["lastGeneratedDate"] = "2026-07-31"
    st["arc"]["startedEpisode"] = 9
    st["arc"]["description"] = NEW_ARC_DESC
    c = st["continuity"]
    c[8] = NEW_CONT9
    c[9] = NEW_CONT10
    c[10] = NEW_CONT11
    c[18] = NEW_CONT19
    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("CANON updated:", CANON)
    # 同步其余副本
    for p in OTHER:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        shutil.copyfile(CANON, p)
        print("SYNC ->", p)


if __name__ == "__main__":
    main()
