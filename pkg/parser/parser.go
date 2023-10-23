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
	"github.com/leafney/slack-togo/common/vars"
	"github.com/leafney/slack-togo/model"
	"github.com/leafney/slack-togo/pkg/utils"
	"github.com/slack-go/slack"
	"log"
)

// 获取历史消息列表
func ParseConversationHistory(data *slack.GetConversationHistoryResponse) []*model.History {
	result := make([]*model.History, 0)

	if data.Ok {
		messages := data.Messages

		for _, m := range messages {
			mId := m.ClientMsgID
			mBot := m.BotID
			//isBot := false
			//if rose.StrIsEmpty(mId) && !rose.StrIsEmpty(mBot) {
			//	isBot = true
			//}

			senderType := vars.SenderTypeUser
			if rose.StrIsEmpty(mId) && !rose.StrIsEmpty(mBot) {
				senderType = vars.SenderTypeAsUser

				subType := m.SubType
				if rose.StrEqualFull(subType, vars.TYPE_BOT_ADD) {
					senderType = vars.SenderTypeBot
				}
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

			// create ts
			createTs := rose.StrToInt64(utils.StrAnySplitFirst(m.Timestamp, "."))

			// edit ts
			editTs := int64(0)
			if m.Edited != nil {
				tmpETS := m.Edited.Timestamp
				log.Println(tmpETS)
				editTs = rose.StrToInt64(utils.StrAnySplitFirst(tmpETS, "."))
			}

			// second items

			item := &model.History{
				MsgId: mId,
				//IsBot:       isBot,
				SType:       senderType,
				MType:       m.Type,
				Text:        m.Text,
				User:        m.User,
				Team:        m.Team,
				Ts:          m.Timestamp,
				ThreadTs:    m.ThreadTimestamp,
				CreateTs:    createTs,
				EditTs:      editTs,
				ReplyCount:  m.ReplyCount,
				Reactions:   emojiList,
				Files:       fileList,
				LatestReply: m.LatestReply,
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

		if !rose.StrIsEmpty(mParentId) {
			isReply = true
		}

		if onlyReply && !isReply {
			continue
		}

		mId := m.ClientMsgID
		mBot := m.BotID

		senderType := vars.SenderTypeUser
		if rose.StrIsEmpty(mId) && !rose.StrIsEmpty(mBot) {
			senderType = vars.SenderTypeAsUser

			subType := m.SubType
			if rose.StrEqualFull(subType, vars.TYPE_BOT_ADD) {
				senderType = vars.SenderTypeBot
			}
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

		// create ts
		createTs := rose.StrToInt64(utils.StrAnySplitFirst(m.Timestamp, "."))

		// edit ts
		editTs := int64(0)
		if m.Edited != nil {
			tmpETS := m.Edited.Timestamp
			log.Println(tmpETS)
			editTs = rose.StrToInt64(utils.StrAnySplitFirst(tmpETS, "."))
		}

		item := &model.History{
			IsReply:     isReply,
			MsgId:       mId,
			SType:       senderType,
			MType:       m.Type,
			Text:        m.Text,
			User:        m.User,
			Team:        m.Team,
			Ts:          m.Timestamp,
			ThreadTs:    m.ThreadTimestamp,
			CreateTs:    createTs,
			EditTs:      editTs,
			Reactions:   emojiList,
			Files:       fileList,
			LatestReply: m.LatestReply,
		}
		result = append(result, item)
	}

	return result
}
