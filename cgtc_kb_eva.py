# encoding: utf-8

# Usage: python cgtc_kb_eva.py test/test.txt test/ref.test.txt test/test.kb.jsonl result.txt

import json
import sys
from difflib import SequenceMatcher

# 读txt文件
def rdt(fp):
	with open(fp, 'r', encoding='utf-8') as rtf:
		return [l.strip() for l in rtf.readlines()]

# 读jsonl文件
def rdj(fp):
	with open(fp, 'r', encoding='utf-8') as rjf:
		return [json.loads(l) for l in rjf.readlines()]

# 抽取kb.jsonl中的知识库条目
def get_kb_terms(kbd, spset=set(["地域信息", "事件信息", "领导人信息"])):

	# 存储kb.jsonl中所有的知识库条目
	rs = []  

	# 提取kb.jsonl中所有的知识库条目
	for key, value in kbd.items():
		if isinstance(value, list):
			if key in spset:
				# 特殊处理地域信息、领导人信息和事件信息的知识库条目
				rs.extend([v[0] if key == "事件信息" else v[-1] for v in value])
			else:
				rs.extend(value)
		elif isinstance(value, str):
			rs.append(value)

	return rs

# 在字符串strin中查找子字符串stf的所有位置，并返回这些位置的索引集合
def find_pos(strin, stf):

	rs = []
	# 找到stf在strin中第一次出现的位置
	_ = strin.find(stf)
	relpos = 0
	_l = len(stf)
	while _ >= 0:
		# 更新relpos为上次找到的位置之后的位置，继续查找stf的下一次出现
		_ += relpos
		_eid = _ + _l
		rs.extend(list(range(_, _eid)))
		relpos = _eid
		_ = strin[relpos:].find(stf)

	return set(rs)

# 在strin中查找知识库条目列表kbtl中的所有条目，并返回这些条目在strin中所有出现位置的索引集合
def find_kb_pos(strin, kbtl):

	rs = set()
	for _ in kbtl:
		rs |= find_pos(strin, _, relpos=0)

	return rs
	
# eops:编辑操作序列;kbpos:知识库条目位置集合;ref:参考文本
# 根据eops和kbpos，提取ref中与知识库条目相关的编辑操作位置，并返回这些位置在生成文本中的对应位置集合rsp以及相关的编辑操作信息rskb
def get_spos_fkb(eops, kbpos, ref):

	rsp = []
	rskb = []
	for tag, ia, ib, ja, jb in eops:
		if (set(range(ia, ib)) & kbpos) or (tag == "insert" and (ia in kbpos)):
			# 生成文本中与知识库条目相关的编辑操作位置集合
			rsp.extend(list(range(ja, jb)))
			# 相关的编辑操作信息，包含操作类型、位置范围和参考文本中的对应内容
			rskb.append((tag, ja, jb, ref[ia:ib],))

	return set(rsp), set(rskb)

# 评估
def eva(src_ss, ref_ss, kb_s, rs_ss):
	TP = 0
	FN = 0
	FP = 0
	TN = 0

	for src, ref, kb, rs in zip(src_ss, ref_ss, kb_s, rs_ss):
		for kb_term in set(get_kb_terms(kb)):
			_sm = SequenceMatcher(None, ref, src, autojunk=False)
			_spos, _redt = get_spos_fkb([_ for _ in _sm.get_opcodes() if (_[0] != "equal")], find_pos(ref, kb_term), ref)
			_sm.set_seq1(rs)
			_rspos = find_pos(rs, kb_term)
			_sedt = set([(_[0], _[-2], _[-1], rs[_[1]:_[2]],) for _ in _sm.get_opcodes() if (_[0] != "equal") and ((set(range(_[-2], _[-1])) & _spos) or (set(range(_[1], _[2])) and _rspos))])#?
			#print(_redt,_sedt)
			TP += len(_redt & _sedt)
			FN += len(_redt - _sedt)
			FP += len(_sedt - _redt)
			if len(find_pos(ref, kb_term)) == 0 and len(find_pos(rs, kb_term)) == 0:
				TN += 1

	# 计算指标
	ACC = float(TP + TN) / float(TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0.0
	P = float(TP) / float(TP + FP) if (TP + FP) > 0 else 0.0
	R = float(TP) / float(TP + FN) if (TP + FN) > 0 else 0.0
	F0_5 = (1.25 * P * R) / (0.25 * P + R) if (0.25 * P + R) > 0 else 0

	return {
		'ACC': ACC,
		'P': P,
		'R': R,
		'F0.5': F0_5
	}

def main(src_ss, ref_ss, kb_s, rs_ss):

	result = eva(rdt(src_ss), rdt(ref_ss), rdj(kb_s), rdt(rs_ss))
	print('最终评估结果：')
	print(f'准确率 (ACC): {result["ACC"] * 100:.2f}%')
	print(f'精确率 (P): {result["P"] * 100:.2f}%')
	print(f'召回率 (R): {result["R"] * 100:.2f}%')
	print(f'F0.5: {result["F0.5"] * 100:.2f}%')

if __name__ == '__main__':
	main(*sys.argv[1:5])
