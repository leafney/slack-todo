/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-10-23 09:25
 * @Description:
 */

package utils

import "github.com/leafney/rose"

func StrAnySplitFirst(s string, seps ...string) string {
	strs := rose.StrAnySplit(s, seps...)
	if len(strs) > 0 {
		return strs[0]
	}
	return ""
}
