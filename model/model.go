/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-23 17:58
 * @Description:
 */

package model

type (
	History struct {
		MsgId string `json:"msg_id"`
		//IsBot       bool            `json:"is_bot"`
		SType       int             `json:"s_type"` // 发布者类型 1用户 2机器人 3模拟用户
		MType       string          `json:"m_type"`
		Text        string          `json:"text"`
		User        string          `json:"user"`
		Team        string          `json:"team"`
		Ts          string          `json:"ts"`
		ThreadTs    string          `json:"thread_ts"`
		CreateTs    int64           `json:"create_ts"`   // 创建时间戳
		EditTs      int64           `json:"edit_ts"`     // 编辑时间戳
		ReplyCount  int             `json:"reply_count"` // 回复项数量
		Reactions   []string        `json:"reactions"`
		Files       []*FileItemInfo `json:"files"`
		IsReply     bool            `json:"is_reply"`     // 是否为回复项
		LatestReply string          `json:"latest_reply"` // 最新回复时间，为空则没有回复
	}

	FileItemInfo struct {
		Id          string `json:"id"`
		Title       string `json:"title"`
		Size        int    `json:"size"`
		UrlDownload string `json:"url_download"`
		UrlPreview  string `json:"url_preview"`
	}
)
