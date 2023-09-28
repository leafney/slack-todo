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
		MsgId      string          `json:"msg_id"`
		IsBot      bool            `json:"is_bot"`
		MType      string          `json:"m_type"`
		Text       string          `json:"text"`
		User       string          `json:"user"`
		Team       string          `json:"team"`
		Ts         string          `json:"ts"`
		ReplyCount int             `json:"reply_count"`
		Reactions  []string        `json:"reactions"`
		Files      []*FileItemInfo `json:"files"`
		IsReply    bool            `json:"is_reply"`
	}

	FileItemInfo struct {
		Id          string `json:"id"`
		Title       string `json:"title"`
		Size        int    `json:"size"`
		UrlDownload string `json:"url_download"`
		UrlPreview  string `json:"url_preview"`
	}
)
