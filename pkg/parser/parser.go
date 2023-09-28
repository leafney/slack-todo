/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-24 08:17
 * @Description:
 */

package parser

import (
	"github.com/leafney/rose"
	"github.com/leafney/slack-togo/model"
	"github.com/slack-go/slack"
)

func ParseConversationHistory(data *slack.GetConversationHistoryResponse) []*model.History {
	result := make([]*model.History, 0)

	if data.Ok {
		messages := data.Messages

		for _, m := range messages {
			mId := m.ClientMsgID
			mBot := m.BotID
			isBot := false
			if rose.StrIsEmpty(mId) && !rose.StrIsEmpty(mBot) {
				isBot = true
			}
			// emoji
			emojiList := make([]string, 0)
			for _, mr := range m.Reactions {
				emojiList = append(emojiList, mr.Name)
			}

			// files
			fileList := make([]*model.FileItemInfo, 0)
			for _, mf := range m.Files {
				fileList = append(fileList, &model.FileItemInfo{
					Id:          mf.ID,
					Title:       mf.Title,
					Size:        mf.Size,
					UrlDownload: mf.URLPrivateDownload,
					UrlPreview:  mf.Permalink,
				})
			}

			// second items

			item := &model.History{
				MsgId:      mId,
				IsBot:      isBot,
				MType:      m.Type,
				Text:       m.Text,
				User:       m.User,
				Team:       m.Team,
				Ts:         m.Timestamp,
				ReplyCount: m.ReplyCount,
				Reactions:  emojiList,
				Files:      fileList,
			}
			result = append(result, item)
		}
	}

	return result
}

// onlyReply: 是否仅包含回复的列表项
func ParseConversationReplies(data []slack.Message, onlyReply bool) []*model.History {
	result := make([]*model.History, 0)

	for _, m := range data {
		// reply item
		isReply := false
		mParentId := m.ParentUserId
		if onlyReply {
			if rose.StrIsEmpty(mParentId) {
				continue
			} else {
				isReply = true
			}
		}

		mId := m.ClientMsgID

		// emoji
		emojiList := make([]string, 0)
		for _, mr := range m.Reactions {
			emojiList = append(emojiList, mr.Name)
		}

		// files
		fileList := make([]*model.FileItemInfo, 0)
		for _, mf := range m.Files {
			fileList = append(fileList, &model.FileItemInfo{
				Id:          mf.ID,
				Title:       mf.Title,
				Size:        mf.Size,
				UrlDownload: mf.URLPrivateDownload,
				UrlPreview:  mf.Permalink,
			})
		}

		item := &model.History{
			IsReply:   isReply,
			Text:      m.Text,
			MsgId:     mId,
			MType:     m.Type,
			User:      m.User,
			Team:      m.Team,
			Ts:        m.Timestamp,
			Reactions: emojiList,
			Files:     fileList,
		}
		result = append(result, item)
	}

	return result
}
